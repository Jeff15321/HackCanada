"""
initial prompt -> loop: {
    Prompt Generator Agent -> [any number of intermediate agents...] -> Consolidator Agent -> Completeness Agent
}
-> final prompt -> final output

toggle-able parts:
- intermediate agents
- number of rounds/loops
- model

to add: proper logging mechanism
"""

from agents import *

import os
import argparse

intermediate_agents = ["Clarity Agent", "Relevance Agent", "Precision Agent", "Creativity Agent", "Contextualization Agent", "Engagement Agent", "Brevity Agent"]

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', type=str, default='Come up with Python exercises/ideas for a class for somebody that has just learned the basics', help='prompt that is to be refined')
    parser.add_argument('--rounds', type=int, default=3, help='number of rounds')
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help='model name as specified by api documentation')
    return parser

def runMultiagentPrompting(prompt, intermediate_agents, rounds, model):
    agents_dict = initialize_prompt_agents(intermediate_agents, model)
    
    print("***** Original Prompt *****")
    print(prompt)
    print("\n")

    prompt = agents_dict["Prompt Generator Agent"].run_api(prompt)
    print("***** Prompt Generator Agent *****")
    print(prompt)
    print("\n")
    print("\n")

    combined_refinements = []
    for i in range(1, rounds+1):
        print("---------------")
        print(f"Intermediate Round {i}")
        print("---------------")
        for intermediate_agent in agents_dict["Intermediate Agents"]:
            refined_prompt = intermediate_agent.run_api(prompt)
            combined_refinements.append(f"agent name: {intermediate_agent.name}, agent role: {intermediate_agent.role}, prompt generated: {refined_prompt}")
            print(f"***** {intermediate_agent.name} *****")
            print(refined_prompt)

        combined_refinements_prompt = f"Original prompt: " + prompt + " | " + " | ".join(combined_refinements)
        prompt = agents_dict["Consolidator Agent"].run_api(prompt)
        print(f"***** Consolidator Agent *****")
        print(prompt)

        prompt = agents_dict["Completeness Agent"].run_api(prompt)
        print("***** Completeness Agent *****")
        print(prompt)

        print("\n")
        print("\n")



if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    runMultiagentPrompting(args.prompt, intermediate_agents, args.rounds, args.model)