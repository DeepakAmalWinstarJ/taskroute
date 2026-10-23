"""TaskRoute AI tools: three specialized tools for programming help.

debug_tool: programming errors and debugging.
learn_tool: explanations of programming concepts.
career_tool: interview and placement preparation.
"""

from __future__ import annotations

from strands import tool


@tool
def debug_tool(error_message: str, code_snippet: str | None = None, language: str = "python") -> dict:
    """Analyze programming errors and suggest debugging steps."""
    # Simple error categorization and debugging advice
    error_lower = error_message.lower()
    
    suggestions = []
    
    # Common error patterns
    if "syntax" in error_lower:
        suggestions.append("Check for missing parentheses, brackets, or quotes")
        suggestions.append("Verify indentation (especially in Python)")
        suggestions.append("Look for typos in keywords or variable names")
    elif "undefined" in error_lower or "not defined" in error_lower:
        suggestions.append("Check if the variable/function is declared before use")
        suggestions.append("Verify import statements are correct")
        suggestions.append("Check for typos in the name")
    elif "type" in error_lower and "error" in error_lower:
        suggestions.append("Check data types of variables being operated on")
        suggestions.append("Convert types if necessary (str(), int(), etc.)")
        suggestions.append("Verify function expects correct argument types")
    elif "index" in error_lower and ("out of range" in error_lower or "bounds" in error_lower):
        suggestions.append("Check the length/size of the array/list before accessing")
        suggestions.append("Verify loop boundaries")
        suggestions.append("Consider off-by-one errors")
    elif "import" in error_lower and ("cannot" in error_lower or "failed" in error_lower):
        suggestions.append("Verify the module is installed (pip install <module>)")
        suggestions.append("Check if module name is spelled correctly")
        suggestions.append("Check Python path/environment")
    else:
        suggestions.append("Read the error message carefully for clues")
        suggestions.append("Search online for the exact error text")
        suggestions.append("Add print statements to trace execution flow")
        suggestions.append("Use a debugger to step through the code")
    
    # Add language-specific advice
    if language == "python":
        suggestions.append("Python: Check indentation (consistent spaces/tabs)")
        suggestions.append("Python: Verify proper colon usage after if/for/def statements")
    elif language == "javascript":
        suggestions.append("JavaScript: Check for missing semicolons")
        suggestions.append("JavaScript: Verify variable scope (let/const/var)")
    elif language == "java":
        suggestions.append("Java: Check class/method visibility (public/private)")
        suggestions.append("Java: Verify proper imports and package structure")
    
    return {
        "error_type": "debugging_assistance",
        "original_error": error_message,
        "language": language,
        "debugging_steps": suggestions,
        "quick_checklist": [
            "✓ Restart your development environment",
            "✓ Check for recent changes to the code",
            "✓ Search online for the exact error message",
            "✓ Simplify the code to isolate the issue"
        ]
    }



@tool
def learn_tool(concept: str, level: str = "beginner", examples: bool = True) -> dict:
    """Explain programming concepts with clear examples."""
    # Common programming concepts database
    explanations = {
        "variables": {
            "beginner": "Variables are like labeled boxes that store data. You put something in the box and give it a name so you can find it later.",
            "intermediate": "Variables are named memory locations that hold values. They have a data type that determines what kind of data they can store.",
            "advanced": "Variables are symbolic names bound to memory addresses, with type systems ensuring type safety and memory management."
        },
        "functions": {
            "beginner": "Functions are reusable pieces of code that perform a specific task. Like a recipe you can use many times.",
            "intermediate": "Functions encapsulate behavior, accept parameters, return values, and promote code reuse and modularity.",
            "advanced": "Functions are first-class citizens in many languages, supporting higher-order functions, closures, and functional programming patterns."
        },
        "loops": {
            "beginner": "Loops repeat code multiple times. Like telling someone 'do this 10 times' instead of writing the same thing 10 times.",
            "intermediate": "Loops iterate over sequences with for-loops or continue while conditions are true with while-loops.",
            "advanced": "Loops involve iteration protocols, lazy evaluation in functional languages, and can be expressed via recursion or higher-order functions."
        },
        "conditionals": {
            "beginner": "Conditionals help programs make decisions. Like 'if it's raining, take an umbrella; otherwise, wear sunglasses.'",
            "intermediate": "Conditional statements (if/else/switch) control program flow based on boolean expressions and comparison operations.",
            "advanced": "Conditionals implement branching logic, with short-circuit evaluation, pattern matching, and guard clauses as advanced forms."
        },
        "arrays": {
            "beginner": "Arrays are lists of items. Like a shelf with numbered compartments where you can store things.",
            "intermediate": "Arrays are contiguous memory structures storing homogeneous elements, accessible via index with O(1) random access.",
            "advanced": "Arrays support various operations (map, filter, reduce), with implementations differing in mutability, dimensionality, and memory layout."
        },
        "objects": {
            "beginner": "Objects combine related data and actions. Like a car object with properties (color, model) and actions (drive, honk).",
            "intermediate": "Objects encapsulate state (properties) and behavior (methods), supporting inheritance, polymorphism, and encapsulation.",
            "advanced": "Objects implement prototypal or class-based inheritance, message passing, and follow design patterns for reusable solutions."
        }
    }
    
    concept_lower = concept.lower()
    
    # Find best matching concept
    matched_concept = None
    for key in explanations:
        if key in concept_lower or concept_lower in key:
            matched_concept = key
            break
    
    if not matched_concept:
        # Generic explanation for unknown concepts
        explanation = f"""A {concept} is a fundamental programming concept that helps organize and structure code.

Key characteristics:
• Provides a way to solve common programming problems
• Follows established patterns and best practices
• Makes code more readable, maintainable, and efficient

To learn more about {concept}:
1. Search for tutorials with practical examples
2. Try implementing it in a small project
3. Compare with similar concepts to understand differences
4. Read official documentation for your programming language"""
        
        example_text = f"Example: In many languages, {concept} helps manage complexity by providing a clear structure for solving specific types of problems."
    else:
        explanation = explanations[matched_concept].get(level, explanations[matched_concept]["beginner"])
        example_text = f"Example: In Python, {matched_concept} are implemented with clear syntax that makes them easy to use and understand."
    
    response = {
        "concept": concept,
        "level": level,
        "explanation": explanation,
        "key_points": [
            "Helps organize code and solve problems",
            "Follows programming best practices",
            "Makes code more readable and maintainable"
        ]
    }
    
    if examples:
        response["examples"] = [
            f"Basic {concept} example for {level} level",
            f"Real-world use case of {concept}",
            f"Common mistakes to avoid with {concept}"
        ]
        response["example_text"] = example_text
    
    return response



@tool
def career_tool(topic: str, experience_level: str = "entry", specific_question: str | None = None) -> dict:
    """Provide career advice for programming interviews and placement preparation."""
    
    advice_categories = {
        "resume": {
            "entry": [
                "Include relevant coursework and academic projects",
                "List programming languages and technologies you're comfortable with",
                "Add any internships, even if unrelated to tech",
                "Include GitHub profile with sample projects"
            ],
            "mid": [
                "Focus on impact and achievements, not just responsibilities",
                "Quantify results (e.g., 'improved performance by 30%')",
                "Highlight leadership and mentorship experience",
                "Tailor resume to specific job descriptions"
            ],
            "senior": [
                "Emphasize architectural decisions and system design",
                "Show leadership in cross-functional teams",
                "Demonstrate business impact of technical decisions",
                "Include publications, talks, or open-source contributions"
            ]
        },
        "interview": {
            "entry": [
                "Practice basic data structures (arrays, linked lists, stacks, queues)",
                "Understand time and space complexity (Big O notation)",
                "Practice solving problems on LeetCode or HackerRank",
                "Prepare behavioral questions using STAR method"
            ],
            "mid": [
                "Master system design fundamentals",
                "Practice medium to hard algorithm problems",
                "Prepare for system design interviews",
                "Be ready to discuss past projects in depth"
            ],
            "senior": [
                "Focus on system architecture and scalability",
                "Prepare for leadership and behavioral questions",
                "Be ready to discuss trade-offs in technical decisions",
                "Practice whiteboard design sessions"
            ]
        },
        "skills": {
            "entry": [
                "Master one programming language deeply",
                "Learn version control (Git)",
                "Understand basic database concepts",
                "Learn testing fundamentals"
            ],
            "mid": [
                "Develop expertise in your tech stack",
                "Learn cloud platform basics (AWS/Azure/GCP)",
                "Understand CI/CD pipelines",
                "Learn containerization (Docker)"
            ],
            "senior": [
                "Develop architectural patterns knowledge",
                "Learn about microservices and distributed systems",
                "Understand security best practices",
                "Learn about monitoring and observability"
            ]
        },
        "networking": {
            "entry": [
                "Create a LinkedIn profile with complete information",
                "Attend local meetups and tech events",
                "Connect with alumni from your school",
                "Participate in online coding communities"
            ],
            "mid": [
                "Build a professional network in your industry",
                "Consider speaking at meetups or conferences",
                "Mentor junior developers",
                "Contribute to open source projects"
            ],
            "senior": [
                "Establish thought leadership through blogs/talks",
                "Build relationships with recruiters and hiring managers",
                "Participate in technical advisory roles",
                "Network with other senior engineers and architects"
            ]
        }
    }
    
    topic_lower = topic.lower()
    matched_topic = "interview"  # default
    
    for key in advice_categories:
        if key in topic_lower:
            matched_topic = key
            break
    
    advice_list = advice_categories[matched_topic].get(experience_level, advice_categories[matched_topic]["entry"])
    
    # Add specific advice based on the question
    specific_advice = []
    if specific_question:
        specific_advice.append(f"For your specific question about '{specific_question}':")
        specific_advice.append("1. Research common approaches and solutions")
        specific_advice.append("2. Practice explaining your thought process clearly")
        specific_advice.append("3. Prepare examples from your experience")
        specific_advice.append("4. Be honest about what you don't know")
    
    return {
        "topic": topic,
        "experience_level": experience_level,
        "advice_category": matched_topic,
        "specific_advice": advice_list,
        "additional_tips": [
            "Practice regularly and consistently",
            "Get feedback from peers or mentors",
            "Stay updated with industry trends",
            "Build a portfolio of projects"
        ],
        "resources": [
            "LeetCode/HackerRank for coding practice",
            "System Design Primer on GitHub",
            "Tech interview handbooks",
            "Mock interview platforms"
        ]
    }


TOOLS = [debug_tool, learn_tool, career_tool]