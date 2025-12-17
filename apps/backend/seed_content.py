import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.domains.study.repository import TopicRepository
from app.domains.subject.repository import SubjectRepository
from app.domains.study.models import User

# Sample Data matching User screenshot
SUBJECTS_DATA = [
    {
        "name": "Physics",
        "slug": "physics",
        "is_featured": True,
        "topics": [
            {
                "title": "Newton's Laws", 
                "slug": "newtons-laws", 
                "description": "Understanding motion and forces",
                "content": "Newton's laws of motion constitute three physical laws that lay the foundation for classical mechanics."
            },
            {
                "title": "Projectiles", 
                "slug": "projectiles", 
                "description": "Motion in two dimensions",
                "content": "Projectile motion is a form of motion experienced by an object or particle that is projected near the Earth's surface and moves along a curved path under the action of gravity only."
            },
            {
                "title": "Electricity", 
                "slug": "electricity", 
                "description": "Current, voltage, and circuits",
                "content": "Electricity is the set of physical phenomena associated with the presence and motion of matter that has a property of electric charge."
            },
            {
                "title": "Light Waves", 
                "slug": "light-waves", 
                "description": "Properties of light and waves",
                "content": "Light denotes electromagnetic radiation of any wavelength, whether visible or not."
            },
            {
                "title": "Energy", 
                "slug": "energy", 
                "description": "Work, power, and energy conservation",
                "content": "In physics, energy is the quantitative property that is transferred to a body or to a physical system, recognizable in the performance of work and in the form of heat and light."
            }
        ]
    },
    {
        "name": "Chemistry",
        "slug": "chemistry",
        "is_featured": True,
        "topics": [
            {
                "title": "Atomic Structure",
                "slug": "atomic-structure",
                "description": "Atoms, protons, neutrons, and electrons",
                "content": "An atom is the smallest unit of ordinary matter that forms a chemical element."
            },
            {
                "title": "Periodic Table",
                "slug": "periodic-table",
                "description": "Elements and their properties",
                "content": "The periodic table is a tabular display of the chemical elements."
            },
            {
                "title": "Chemical Bonding",
                "slug": "chemical-bonding",
                "description": "Ionic, Covalent, and Metallic bonds",
                "content": "A chemical bond is a lasting attraction between atoms, ions or molecules that enables the formation of chemical compounds."
            },
            {
                "title": "Stoichiometry",
                "slug": "stoichiometry",
                "description": "Calculations of reactants and products",
                "content": "Stoichiometry is the calculation of reactants and products in chemical reactions."
            },
            {
                "title": "Acids and Bases",
                "slug": "acids-and-bases",
                "description": "pH, neutralization, and titration",
                "content": "Acids and bases are two special kinds of chemicals."
            }
        ]
    },
    {
        "name": "History",
        "slug": "history",
        "is_featured": True,
        "topics": [
            {
                "title": "World War II",
                "slug": "world-war-ii",
                "description": "Global conflict from 1939 to 1945",
                "content": "World War II was a global war that lasted from 1939 to 1945."
            },
            {
                "title": "Ancient Egypt",
                "slug": "ancient-egypt",
                "description": "Civilization of ancient North Africa",
                "content": "Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River."
            },
            {
                "title": "The Renaissance",
                "slug": "renaissance",
                "description": "European cultural rebirth",
                "content": "The Renaissance was a period in European history marking the transition from the Middle Ages to modernity."
            },
            {
                "title": "Industrial Revolution",
                "slug": "industrial-revolution",
                "description": "Transition to new manufacturing processes",
                "content": "The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States."
            },
            {
                "title": "Cold War",
                "slug": "cold-war",
                "description": "Geopolitical tension between US and USSR",
                "content": "The Cold War was a period of geopolitical tension between the United States and the Soviet Union and their respective allies."
            }
        ]
    },
    {
        "name": "General Knowledge",
        "slug": "general-knowledge",
        "is_featured": True,
        "topics": [
            {
                "title": "Capitals of the World",
                "slug": "world-capitals",
                "description": "Major cities and governments",
                "content": "A capital is the municipality enjoying primary status in a country, state, province, or other administrative region."
            },
            {
                "title": "Solar System",
                "slug": "solar-system",
                "description": "Sun, planets, and celestial bodies",
                "content": "The Solar System is the gravitationally bound system of the Sun and the objects that orbit it."
            },
            {
                "title": "Seven Wonders",
                "slug": "seven-wonders",
                "description": "Ancient and modern wonders",
                "content": "The Seven Wonders of the World is a list of remarkable constructions of classical antiquity."
            }
        ]
    },
    {
        "name": "Technology",
        "slug": "technology",
        "is_featured": True,
        "topics": [
            {
                "title": "Robotics",
                "slug": "robotics",
                "description": "Design, construction, and operation of robots",
                "content": "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electronic engineering, information engineering, computer science, and others."
            },
            {
                "title": "Artificial Intelligence",
                "slug": "artificial-intelligence",
                "description": "Simulation of human intelligence by machines",
                "content": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans."
            },
            {
                "title": "Generative AI",
                "slug": "generative-ai",
                "description": "AI capable of generating text, images, or other media",
                "content": "Generative artificial intelligence (generative AI) is a type of AI system capable of generating text, images, or other media in response to prompts."
            }
        ]
    },
    {
        "name": "Biology",
        "slug": "biology",
        "is_featured": True,
        "topics": [
            {
                "title": "Cell Biology",
                "slug": "cell-biology",
                "description": "Structure and function of cells",
                "content": "Cell biology is the study of cell structure and function, and it revolves around the concept that the cell is the fundamental unit of life."
            },
            {
                "title": "Genetics",
                "slug": "genetics",
                "description": "Genes, heredity, and variation",
                "content": "Genetics is a branch of biology concerned with the study of genes, genetic variation, and heredity in organisms."
            },
            {
                "title": "Ecology",
                "slug": "ecology",
                "description": "Interactions among organisms",
                "content": "Ecology is the study of the relationships between living organisms, including humans, and their physical environment."
            }
        ]
    },
    {
        "name": "Mathematics",
        "slug": "mathematics",
        "is_featured": True,
        "topics": [
            {
                "title": "Algebra",
                "slug": "algebra",
                "description": "Symbols and rules for manipulating them",
                "content": "Algebra is one of the broad parts of mathematics, together with number theory, geometry and analysis."
            },
            {
                "title": "Geometry",
                "slug": "geometry",
                "description": "Shapes, sizes, and properties of space",
                "content": "Geometry is a branch of mathematics that deals with questions of shape, size, relative position of figures, and the properties of space."
            },
            {
                "title": "Calculus",
                "slug": "calculus",
                "description": "Continuous change",
                "content": "Calculus is the mathematical study of continuous change, in the same way that geometry is the study of shape and algebra is the study of generalizations of arithmetic operations."
            }
        ]
    },

    {
        "name": "English",
        "slug": "english",
        "is_featured": True,
        "topics": [
            {
                "title": "English Grammar",
                "slug": "english-grammar",
                "description": "Rules of language",
                "content": "Grammar is the system and structure of a language. The grammar of a language includes basic axioms such as the existence of tenses of verbs, articles and adjectives and their proper order, how questions are phrased, and much more."
            },
            {
                "title": "Literature",
                "slug": "literature",
                "description": "Study of written works",
                "content": "Literature is any collection of written work, but it is also used more narrowly for writings specifically considered to be an art form, especially prose fiction, drama, and poetry."
            },
            {
                "title": "Creative Writing",
                "slug": "creative-writing",
                "description": "Art of writing",
                "content": "Creative writing is any writing that goes outside the bounds of normal professional, journalistic, academic, or technical forms of literature, typically identified by an emphasis on narrative craft, character development, and the use of literary tropes or with various traditions of poetry and poetics."
            }
        ]
    },
    {
        "name": "Uncategorized",
        "slug": "uncategorized",
        "is_featured": True,
        "topics": [] 
    }
]

def seed_content():
    db = SessionLocal()
    try:
        subject_repo = SubjectRepository(db)
        topic_repo = TopicRepository(db)

        for subj_data in SUBJECTS_DATA:
            # Check if subject exists
            subject = subject_repo.get_by_slug(subj_data['slug'])
            if not subject:
                subject = subject_repo.create(
                    name=subj_data['name'], 
                    slug=subj_data['slug'], 
                    is_featured=subj_data['is_featured']
                )
                print(f"Created Subject: {subject.name}")
            else:
                print(f"Subject {subject.name} already exists.")

            # Seed Topics
            for t_data in subj_data['topics']:
                existing_topic = topic_repo.get_by_slug_and_subject(t_data['slug'], subject.id)
                if not existing_topic:
                    topic = topic_repo.create(
                        title=t_data['title'],
                        slug=t_data['slug'],
                        subject_id=subject.id,
                        content=t_data['content'],
                        description=t_data['description'],
                        is_featured=True,
                        is_public=True
                    )
                    print(f"Created Topic: {topic.title}")
                else:
                    print(f"Topic {t_data['title']} already exists.")
                    # Update description if missing
                    if not existing_topic.description:
                        existing_topic.description = t_data['description']
                        db.commit()
                        print(f"Updated description for {existing_topic.title}")


    except Exception as e:
        print(f"Error seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_content()
