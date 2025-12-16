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
