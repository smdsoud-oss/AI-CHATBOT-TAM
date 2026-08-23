def analyze_argument(text):
    """
    Break down an argument into logical components
    """
    analysis = {
        "type": "argument_analysis",
        "steps": [
            "1. Identify the main claim",
            "2. Find supporting evidence",
            "3. Check for logical fallacies",
            "4. Evaluate the conclusion"
        ],
        "original": text
    }
    return analysis


def solve_logic_puzzle(puzzle):
    """
    Guide through solving logic puzzles step by step
    """
    steps = f"""
    🧠 Logic Puzzle Breakdown:
    
    Puzzle: {puzzle}
    
    Step 1 → Read carefully and identify what is given
    Step 2 → List all conditions and constraints
    Step 3 → Eliminate impossible options
    Step 4 → Apply deductive reasoning
    Step 5 → Verify your answer against all conditions
    """
    return steps


def identify_fallacies(argument):
    """
    Identify common logical fallacies in an argument
    """
    fallacies = {
        "ad hominem": "attacking the person instead of the argument",
        "straw man": "misrepresenting someone's argument",
        "false dilemma": "presenting only two options when more exist",
        "circular reasoning": "using the conclusion as a premise",
        "hasty generalization": "drawing broad conclusions from few examples",
        "slippery slope": "assuming one event leads to extreme consequences",
        "appeal to authority": "using authority as evidence without proof",
        "bandwagon": "believing something because everyone else does"
    }

    found = []
    argument_lower = argument.lower()

    for fallacy, description in fallacies.items():
        if any(word in argument_lower for word in fallacy.split()):
            found.append(f"⚠️ {fallacy.title()}: {description}")

    if found:
        return "Potential fallacies found:\n" + "\n".join(found)
    else:
        return "✅ No obvious logical fallacies detected."


def critical_thinking_response(user_input):
    """
    Main function called by chatbot for critical thinking tasks
    """
    user_lower = user_input.lower()

    if any(word in user_lower for word in
           ['fallacy', 'fallacies', 'logical error']):
        return identify_fallacies(user_input)

    elif any(word in user_lower for word in
             ['puzzle', 'riddle', 'logic problem']):
        return solve_logic_puzzle(user_input)

    elif any(word in user_lower for word in
             ['analyze', 'analyse', 'argument', 'debate']):
        result = analyze_argument(user_input)
        return f"""
🔍 Argument Analysis:

Original: {result['original']}

Framework:
{chr(10).join(result['steps'])}

Apply these steps to build a strong, logical answer!
Hope that helps! — TAM 💡
        """

    return None