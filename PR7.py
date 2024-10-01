from crfm import crfmChatLLM
# import openai
from langchain_community.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
import random

## list of random problems 

problem_description = "Conflict: A conversation between a customer and employee. The blender is not working and the customer wants to return."


roles = ["employee", "customer"]
goals = ["Resolve the conflict and be helpful", "Be adversarial and aggressive in problem solving"]
strategy_str "Interests, Positive Expectations, Proposal, Concession, Facts, Rights, Power"

context = """Prompt:
You are a chatbot that realistically roleplays a virtual conflict.

Each message must use only one of the following strategies:""" +
strategy_str
+ """

The following positive strategies increase cooperativeness:
- Interests
- Positive Expectations
- Proposal

The following neutral strategies do not change cooperativeness:
- Concession
- Facts

The following negative strategies decrease cooperativeness:
- Rights
- Power

You will roleplay as {simulated_char} or {user_char}. 

{simulated_char} will also have a cooperativeness level from 1 (very uncooperative) - 5 (very cooperative).

Cooperativeness score rules:
- If cooperativeness is low, negative strategies are used.
- If cooperativeness is high, positive strategies are used.
- If several positive strategies are used, {simulated_char} slowly becomes more cooperative.
- Continuing to repeatedly use positive expectations without proposing something will not increase cooperativeness
- {simulated_char} must not use positive strategies or try to solve the problem (e.g. ask questions) until cooperativeness is 3 or greater.
- If negative strategies are used, {simulated_char} will retaliate with a negative strategy.
- Otherwise, {simulated_char}'s cooperativeness will stay the same.

Summary of {simulated_char}:
{simulated_char_details}

Do NOT assume anything about the conversation. Only make inferences based on the summary of {simulated_char} and the prior messages.

Messages must only use one strategy at a time.

Format your message as follows. Only complete the <fill in> fields. Copy all fields that do not have a <fill in> value.

From: <fill in>
Cooperativeness: <fill in>
Strategy: <fill in>
Message: <fill in>



"""




class Student:

    def  __init__(self, role, simulated_char_details) -> None:
        self.role = role
        self.goal = goal
        self.simulated_char = "employee"
        self.simulated_char_details = simulated_char_details
    def get_message(self, instruction, question) -> str:
        system_template = """Follow the instruction from the teacher and respond in the following format:
Thought:<thought>
Message:<answer>
For example:
Thought: <thought>
Message: 

From: <fill in>
Cooperativeness: <fill in>
Strategy: <fill in>
Message: <fill in>

Instruction from teacher: {instruction}"""
        user_template = f"{question}\nInstruction to follow: {instruction}"
        system_message = system_template.format(instruction=instruction)
        user_message = user_template.format(instruction=instruction, question=context)
        messages = [SystemMessage(content=system_message), HumanMessage(content=user_message)]
        response = llm.generate([messages], stop=["Q:"]).generations[0][0].text
        return response.strip()

    def generate_response(self, context, teacher_instructions):
        convo = context.copy()
        # Get the instruction from the teacher
        instruction = random.choice(teacher_instructions)
        response = self.get_message(instruction, convo)
        return response

    
class Opponent:

    def  __init__(self, role, goal, simulated_char_details):
        self.role = role
        self.goal = goal
        self.simulated_char = "customer"
        self.simulated_char_details = simulated_char_details
    def generate_response(self, context):
        convo = context.copy()
        messages = [
            SystemMessage(content=opponent_prompt),
            HumanMessage(content="\n".join(convo))
        ]
        response = llm.generate([messages], stop=["Q:"]).generations[0][0].text
        return response.strip()

class Teacher:
    def  __init__(self, problem) -> None:
      self.problem = problem
      self.mutation_prompt = """Help the employee resolve the conflict in the best way possible for the above problem.
Write possible instructions or strategies that the employee should follow.
Respond in the following format:
Instructions:
1. 
...
n. 
""" 
    def parse_instructions(self, response):
        instructions = response.split("Instuctions:")[-1]
        instructions = [instruction.strip() for instruction in instructions.split('\n')]
        return instructions

    def get_instructions(self):
      ## we need to fix messages here as well, not sure proper syntax 
      ## spit out a list of instructions 
      system_template = "You must come up with strategies to help the employee resolve the conflict. The problem that they see is this: {problem_description}"
      system_message = system_template.format(problem=self.problem)
      messages = [SystemMessage(content=system_message), HumanMessage(content=self.mutation_prompt)]
      instructions = llm.generate([messages], stop=["Q:"]).generations[0][0].text
      instructions = self.parse_instructions(instructions)
      return instructions
    
class Judge: 
    def  __init__(self):
        self.prompt = """Two people are having an argument, this will be passed in in the form of a list. 
        The first string is the student, the second string is the opponent and it continues to switch off. 

        Your job is to decide who won the argument. 

        Return student if student won, and opponent if opponent won.

        This is the conversation: 
        
        """
    def generate_response(self, context):
        messages = [
            SystemMessage(content=self.prompt),
            HumanMessage(content="\n".join(context))
        ]
        response = llm.generate([messages], stop=["Q:"]).generations[0][0].text
        return response.strip()

# Initialize the Teacher
teacher = Teacher(problem_description)
teacher_instructions = teacher.get_instructions()

student = Student(role=roles[0], goal=goals[0], simulated_char_details="Employee who is trying to be helpful and cooperative.")
opponent = Opponent(role=roles[1], goal=goals[1], simulated_char_details="Customer who is adversarial and less cooperative.")


llm = crfmChatLLM(model_name=f"openai/gpt-4-0613")

opponent = Opponent()

# initialize student agent
student = Student(role[0])

# print(question)
teacher = Teacher(question)



conversation_history = []

for i in range(5):
    student_response = student.generate_response(conversation_history, teacher_instructions)
    conversation_history.append(student_response)
    opponent_response = opponent.generate_response(conversation_history)
    conversation_history.append(opponent_response)



