import dspy
from sqlalchemy.orm import Session
from .prompts import StudyChat, TopicExplainer, ChatSummarizer
from .tools import Calculator, CurrentTime
from app.config.llm import get_lm_for_locale
from app.domains.study.repository import StudyRepository, TopicRepository, ChatRepository, UserRepository
from app.domains.subject.repository import SubjectRepository
from app.domains.study.models import Topic, User, ChatSession

def get_full_language_name(code: str) -> str:
    mapping = {
        "pcm": "Broken English",
        "pidgin": "Broken English",
        "ha": "Hausa",
        "ig": "Igbo",
        "yo": "Yoruba",
        "en": "English"
    }
    return mapping.get(code.lower(), code)

class StudyAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.tools = [Calculator(), CurrentTime()]
        self.react = dspy.ReAct(StudyChat, tools=self.tools)
        self.summarizer = dspy.ChainOfThought(ChatSummarizer)

    def forward(self, history: list, question: str, language: str):
        full_language = get_full_language_name(language)
        history_str = ""
        for msg in history:
            role = msg.get("sender", msg.get("role", "user")) 
            content = msg.get("content", "")
            history_str += f"{role}: {content}\n"
            
        return self.react(history=history_str, question=question, language=full_language)

    def summarize(self, history: list, language: str):
        full_language = get_full_language_name(language)
        history_str = ""
        for msg in history:
            role = msg.get("sender", msg.get("role", "user"))
            content = msg.get("content", "")
            history_str += f"{role}: {content}\n"
        
        return self.summarizer(conversation_history=history_str, language=full_language)

class StudyService:
    def __init__(self, db: Session):
        self.db = db
        self.module = StudyAgent()
        self.topic_repo = TopicRepository(db)
        self.chat_repo = ChatRepository(db)
        self.subject_repo = SubjectRepository(db)
        self.user_repo = UserRepository(db)

    async def get_or_create_topic(self, subject_id: str, title: str, user: User, language: str = "english", context_instruction: str = None, description: str = None) -> Topic:
        """
        Get existing topic (by Title rough match or generated slug) or Create new one with LLM content.
        """
        # Setup LLM Context immediately
        lm = get_lm_for_locale(language)
        context_manager = dspy.context(lm=lm) if lm else dspy.context()
        
        full_language = get_full_language_name(language)
        explainer = dspy.ChainOfThought(TopicExplainer)
        self._load_pidgin_demos(explainer) # Optimization

        default_context = "Do not include the topic title as a heading. Start directly with the definition or explanation. Structure the response clearly with headings for 'What is it?', 'Key Concepts', 'Common Misconceptions', and 'Exam Notes (JAMB/WAEC)'."
        final_context = context_instruction or default_context

        # 1. Check simplistic Slug match first
        simple_slug = title.lower().strip().replace(" ", "-") # Very basic
        existing = self.topic_repo.get_by_slug_and_subject(simple_slug, subject_id)
        
        if existing:
            # STRICT NORMALIZATION: Always check translation table
            translation = self.topic_repo.get_translation(existing.id, language)
            if translation:
                 # Populate content for response flexibility (though strictly we return Topic + Content usually separate, but models expect topic.content)
                 existing.content = translation.content
                 return existing
            
            # Generate missing translation (even if language is English but missing in translations table)
            with context_manager:
                prediction = explainer(topic=title, language=full_language, context=final_context)
            self.topic_repo.add_translation(existing.id, language, prediction.explanation)
            existing.content = prediction.explanation
            return existing

        # 2. Generate Content & Slug using LLM (if not existing)
        with context_manager:
            prediction = explainer(topic=title, language=full_language, context=final_context)
            
        generated_slug = prediction.slug
        content = prediction.explanation
        
        # Fallback slug if LLM failed
        if not generated_slug:
            generated_slug = simple_slug
        
        # Check existence by generated slug
        existing_by_slug = self.topic_repo.get_by_slug_and_subject(generated_slug, subject_id)
        if existing_by_slug:
             # Check translation 
             translation = self.topic_repo.get_translation(existing_by_slug.id, language)
             if translation:
                 existing_by_slug.content = translation.content
                 return existing_by_slug
             
             self.topic_repo.add_translation(existing_by_slug.id, language, content)
             existing_by_slug.content = content
             return existing_by_slug
            
        # Create Topic (Metadata)
        topic = self.topic_repo.create(
            title=title,
            slug=generated_slug,
            subject_id=subject_id,
            content=None, # LEGACY: Content now lives in translations. topic.content is legacy/fallback.
            description=description, 
            user_id=user.id,
            is_public=True,
            is_featured=False,
            language=language # Original language metadata
        )
        
        # ALWAYS ADD TRANSLATION (Normalized)
        self.topic_repo.add_translation(topic.id, language, content)
        
        # Populate for return
        topic.content = content
             
        return topic

    async def get_topic_by_id(self, topic_id: str, language: str = "english") -> Topic:
        topic = self.topic_repo.get_by_id(topic_id)
        if not topic:
            return None
            
        # NORMALIZE: Fetch content from translation
        translation = self.topic_repo.get_translation(topic.id, language)
        if translation:
            topic.content = translation.content
        else:
            # If requested language missing, maybe fallback to topic language?
            # Or return None for content? 
            # For now, let's try to get content in Topic's native language as fallback
            # But strictly, we should probably return empty or original if same.
            fallback = self.topic_repo.get_translation(topic.id, topic.language)
            if fallback:
                topic.content = fallback.content
            # If even fallback missing (shouldn't happen with migration), topic.content is naturally whatever DB has (which is legacy value)
            
        return topic
    
    async def start_chat_session(self, user: User, topic_id: str, topic_name: str = None, initial_context: str = None, language: str = "english") -> ChatSession:
        
        # 1. Reuse existing session if available for this topic
        existing = self.chat_repo.get_session_by_user_and_topic(user.id, topic_id)
        if existing:
            # If session exists, we resume it. 
            # We do NOT re-seed the context as history already exists.
            return existing

        # 2. Create new session
        session = self.chat_repo.create_session(user.id, topic_id)
        
        # 3. Seed History (Localized)
        if topic_name and initial_context:
            # Localize the "Explain" prompt
            lang_lower = language.lower()
            initial_prompt = f"Explain {topic_name}" # Default
            
            if lang_lower in ["yo", "yoruba"]:
                initial_prompt = f"Ṣalaye {topic_name}"
            elif lang_lower in ["ha", "hausa"]:
                initial_prompt = f"Yi bayani akan {topic_name}" # Approximate Hausa
            elif lang_lower in ["ig", "igbo"]:
                initial_prompt = f"Kọwaa {topic_name}"
            elif lang_lower in ["pcm", "pidgin", "broken english"]:
                 initial_prompt = f"Abeg explain {topic_name}"
            
            self.chat_repo.add_message(session.id, "user", initial_prompt)
            self.chat_repo.add_message(session.id, "assistant", initial_context)
            
        return session

    async def get_chat_session(self, session_id: str) -> ChatSession:
        return self.chat_repo.get_session(session_id)

    async def chat(self, session_id: str, message: str, language: str, user: User):
        session = self.chat_repo.get_session(session_id)
        if not session:
             raise ValueError("Session not found")
        
        # Verify ownership
        if session.user_id != user.id:
             raise ValueError("Unauthorized")

        # Get history
        messages = self.chat_repo.get_history(session_id)
        history_list = [{"role": m.role, "content": m.content} for m in messages]
        
        # Add User Message to DB
        self.chat_repo.add_message(session_id, "user", message)
        
        # Call LLM
        lm = get_lm_for_locale(language)
        context_manager = dspy.context(lm=lm) if lm else dspy.context()
        
        # agent = self.module # StudyAgent instance
        # Response
        try:
             with context_manager:
                 prediction = self.module.forward(history=history_list, question=message, language=language)
             answer = prediction.answer
        except Exception as e:
             print(f"Chat Error: {e}")
             answer = "I'm having trouble thinking right now. Please try again."

        # Add AI Message to DB
        self.chat_repo.add_message(session_id, "assistant", answer)
        
        return {
            "answer": answer,
            "session_id": session_id
        }

    async def create_topic_generator(self, subject_id: str, title: str, user: User, language: str = "english", context_instruction: str = None, description: str = None):
        """
        Generator for SSE Topic Creation.
        """
        import json
        import asyncio
        from functools import partial

        # 1. Check simplistic Slug match first
        simple_slug = title.lower().strip().replace(" ", "-")
        existing = self.topic_repo.get_by_slug_and_subject(simple_slug, subject_id)
        
        
        if existing:
            # Topic exists. STRICT NORMALIZATION check.
            content_to_return = None
            
            translation = self.topic_repo.get_translation(existing.id, language)
            if translation:
                content_to_return = translation.content
            else:
                # Yield "Draft" state but with existing ID
                yield "data: " + json.dumps({
                    "id": str(existing.id),
                    "slug": existing.slug,
                    "title": existing.title,
                    "description": description or existing.description,
                    "is_existing": False, # Treat as generating for client loader
                    "is_complete": False
                }) + "\n\n"
                
                # Start Generation for Translation
                await asyncio.sleep(0.1) # Flush
                
                lm = get_lm_for_locale(language)
                context_manager = dspy.context(lm=lm) if lm else dspy.context()
                full_language = get_full_language_name(language)
                explainer = dspy.ChainOfThought(TopicExplainer)
                self._load_pidgin_demos(explainer)
                
                default_context = "Do not include the topic title as a heading. Start directly with the definition or explanation. Structure the response clearly with headings for 'What is it?', 'Key Concepts', 'Common Misconceptions', and 'Exam Notes (JAMB/WAEC)'."
                final_context = context_instruction or default_context

                try:
                    loop = asyncio.get_running_loop()
                    def run_dspy():
                        with context_manager:
                            return explainer(topic=title, language=full_language, context=final_context)
                    
                    prediction = await loop.run_in_executor(None, run_dspy)
                    
                    # Save Translation
                    self.topic_repo.add_translation(existing.id, language, prediction.explanation)
                    content_to_return = prediction.explanation
                    
                except Exception as e:
                    print(f"Translation Failed: {e}")
                    yield "data: " + json.dumps({"error": "Failed to generate translation", "is_complete": True}) + "\n\n"
                    return

            # Yield Result
            yield "data: " + json.dumps({
                "id": str(existing.id),
                "slug": existing.slug,
                "title": existing.title,
                "content": content_to_return,
                "description": description or existing.description,
                "is_existing": True,
                "is_complete": True
            }) + "\n\n"
            return
            
        # 2. Create Draft Topic (New)
        draft_content = "Generating explanation..."
        draft_topic = self.topic_repo.create(
            title=title,
            slug=simple_slug,
            subject_id=subject_id,
            content=None, # LEGACY: Content in translation only
            description=description or f"Explanation of {title}",
            user_id=user.id,
            is_public=False,
            is_featured=False,
            language=language # Persist creation language
        )

        
        # Yield Chunk 1: Metadata
        yield "data: " + json.dumps({
            "id": str(draft_topic.id),
            "slug": draft_topic.slug,
            "title": draft_topic.title,
            "description": draft_topic.description,
            "is_existing": False, 
            "is_complete": False
        }) + "\n\n"

        # Force flush and yield control
        await asyncio.sleep(0.1)

        # 3. Generate Content using LLM (Non-blocking)
        lm = get_lm_for_locale(language)
        context_manager = dspy.context(lm=lm) if lm else dspy.context()
        full_language = get_full_language_name(language)
        explainer = dspy.ChainOfThought(TopicExplainer)
        self._load_pidgin_demos(explainer)
        
        default_context = "Do not include the topic title as a heading. Start directly with the definition or explanation. Structure the response clearly with headings for 'What is it?', 'Key Concepts', 'Common Misconceptions', and 'Exam Notes (JAMB/WAEC)'."
        final_context = context_instruction or default_context

        try:
            loop = asyncio.get_running_loop()
            
            # Helper to run dspy in context
            def run_dspy():
                with context_manager:
                     return explainer(topic=title, language=full_language, context=final_context)

            prediction = await loop.run_in_executor(None, run_dspy)
            
            generated_slug = prediction.slug or simple_slug
            content = prediction.explanation
            
            # 4. Update Topic in DB
            draft_topic.slug = generated_slug
            # draft_topic.content = content # LEGACY: No longer storing here.
            draft_topic.is_public = True # Now public
            self.db.commit()
            
            # ALWAYS Add to translation table (Normalized)
            self.topic_repo.add_translation(draft_topic.id, language, content)

            self.db.refresh(draft_topic)
            
            # Yield Chunk 2: Final Content
            yield "data: " + json.dumps({
                "id": str(draft_topic.id),
                "slug": draft_topic.slug,
                "content": content,
                "is_complete": True
            }) + "\n\n"
            
        except Exception as e:
            print(f"LLM Generation Failed: {e}")
            yield "data: " + json.dumps({
                "error": "Failed to generate content",
                "is_complete": True
            }) + "\n\n"

    def _load_pidgin_demos(self, explainer):
        import json
        import os
        possible_paths = ["optimized_pidgin_explainer.json", "apps/study-chat-server/optimized_pidgin_explainer.json"]
        data = None
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                    break 
                except: pass
        
        if not data: return
        try:
             demos = data.get("generate.predict", {}).get("demos", []) or data.get("demos", [])
             valid_demos = [dspy.Example(**d).with_inputs("topic", "language", "context") for d in demos if d.get("explanation")]
             if valid_demos:
                 if hasattr(explainer, 'predictor'): explainer.predictor.demos = valid_demos
                 explainer.demos = valid_demos
        except: pass