import {
  FlaskConical,
  Atom,
  Scale,
  Calculator,
  BookOpenText,
  Cpu,
} from "lucide-react";

export const SUBJECTS_DATA = [
  {
    id: "chemistry",
    title: "Chemistry",
    icon: FlaskConical,
    topics: [
      {
        id: "electrolysis",
        title: "Electrolysis",
        desc: "Learn about electric current and chemical changes",
      },
      {
        id: "redox",
        title: "Oxidation and Reduction",
        desc: "Understanding electron transfer in reactions",
      },
      {
        id: "stoichiometry",
        title: "Stoichiometry",
        desc: "Calculating quantities in chemical reactions",
      },
      {
        id: "periodic",
        title: "Periodic Table Trends",
        desc: "Patterns in element properties and behavior",
      },
      {
        id: "bonding",
        title: "Chemical Bonding",
        desc: "How atoms join to form compounds",
      },
    ],
  },
  {
    id: "physics",
    title: "Physics",
    icon: Atom,
    topics: [
      {
        id: "motion",
        title: "Laws of Motion",
        desc: "Newton's laws and their applications",
      },
      {
        id: "energy",
        title: "Energy and Work",
        desc: "Conservation of energy and power calculation",
      },
    ],
  },
  {
    id: "government",
    title: "Government",
    icon: Scale,
    topics: [
      {
        id: "democracy",
        title: "Democracy",
        desc: "Principles and practice of democratic rule",
      },
      {
        id: "constitution",
        title: "Constitution",
        desc: "The supreme law of the land",
      },
    ],
  },
  {
    id: "economics",
    title: "Economics",
    icon: Calculator,
    topics: [
      {
        id: "demand_supply",
        title: "Demand and Supply",
        desc: "Market forces and price determination",
      },
      {
        id: "inflation",
        title: "Inflation",
        desc: "Causes and effects of rising prices",
      },
    ],
  },
  {
    id: "literature",
    title: "Literature",
    icon: BookOpenText,
    topics: [
      {
        id: "poetry",
        title: "African Poetry",
        desc: "Analysis of poems by Wole Soyinka and others",
      },
      { id: "drama", title: "Drama", desc: "Elements of dramatic literature" },
    ],
  },
  {
    id: "technology",
    title: "Technology",
    icon: Cpu,
    topics: [
      {
        id: "ai",
        title: "Artificial Intelligence",
        desc: "Elements of artificial intelligence",
      },
      {
        id: "robotics",
        title: "Robotics",
        desc: "Elements of robotics",
      },
      {
        id: "quantum",
        title: "Quantum Computing",
        desc: "Elements of quantum computing",
      },
    ],
  },
];

export const footerLinks = [
  {
    title: "Product",
    links: ["Features", "Pricing", "API", "Integrations"],
  },
  {
    title: "Company",
    links: ["About", "Careers", "Blog", "Press"],
  },
  {
    title: "Resources",
    links: ["Documentation", "Help Center", "Community", "Contact"],
  },
];
