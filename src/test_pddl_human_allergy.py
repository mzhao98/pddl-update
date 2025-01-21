from pddl_parser.planner import PDDL_Parser, Planner
from pddl_parser.action import Action
import re


# write a function to update the actions by adding a new capability
def add_capability(action, capability):
    new_action = Action(action.name, action.parameters, action.positive_preconditions, action.negative_preconditions,
                        action.add_effects, action.del_effects)
    return new_action



# update the actions to include the new capability of the human
# find the action that the human response is related to
# sentence parsing
# do a regex check for "I can"
def process_human_response(initial_goal, human_response):
    # Regex patterns
    action_pattern = r"I can (.*?allerg.*?)\."  # Matches "I can" and looks for "allerg"
    goal_pattern = r"We need to (.*?allerg.*?)\."  # Matches "We need to" and looks for "allerg"

    # Check for "I can" to define actions
    action_match = re.search(action_pattern, human_response, re.IGNORECASE)
    if action_match:
        action_description = action_match.group(1).strip()
        actions = [Action('allergy-query', [['?h', 'human'],[ '?rec', 'recipe']], [('recipe-selected', 'recipe1')], [],
        [('allergens-identified','rec')], []),
                   Action('resolve-allergies', [['?h', 'human'], ['?rec', 'recipe']], [('allergens-identified','rec')], [],
                          [('allergen-free', 'recipe1')], [])
                   ]
        additional_predicates = {'allergens-identified': {}, 'allergen-free': {'?r': 'recipe'}}

    else:
        actions = []
        additional_predicates = {}

    # Check for "We need to" to add goal conditions
    goal_match = re.search(goal_pattern, human_response, re.IGNORECASE)
    if goal_match:
        goal_condition = goal_match.group(1).strip()
        additional_goals = [('allergen-free', 'recipe1')]

    else:
        additional_goals = []

    # Adjust initial condition
    init_condition = "()"  # Based on your requirement to change from (allergen-free recipe1) to ()


    return actions, additional_goals, init_condition, additional_predicates


# update the actions
def update_parser(parser, new_actions, additional_predicates, new_goals):
    for act in new_actions:
        parser.actions.append(act)

    # update the predicates
    for new_pred in additional_predicates:
        parser.predicates[new_pred] = additional_predicates[new_pred]

    # update the goal to have the new constraint that the recipe must be announced
    for new_goal in new_goals:
        parser.positive_goals.add(new_goal)

    return parser

if __name__ == '__main__':
    domain = 'init_serving_domain/domain.pddl'
    problem = 'init_serving_domain/problem.pddl'
    parser = PDDL_Parser()
    # print('----------------------------')
    print(parser.scan_tokens(domain))
    # print('----------------------------')
    print(parser.scan_tokens(problem))
    # print('----------------------------')
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    # print('Domain name: ' + str(parser.domain_name))
    #
    # # print what the parser found
    # print('Types: ' + str(parser.types))
    # print('Actions: ' + str(parser.actions))
    # print('Predicates: ' + str(parser.predicates))
    # print('Objects: ' + str(parser.objects))
    # print('Positive goals: ' + str(parser.positive_goals))
    # print('Negative goals: ' + str(parser.negative_goals))
    # print('State: ' + str(parser.state))


    # Example human statement
    human_response = 'We need to check for allergies. I can check for allergies.'

    # Process the statement
    new_actions, new_goals, init_condition, additional_predicates = process_human_response(parser.positive_goals,
                                                                                           human_response)
    parser = update_parser(parser, new_actions, additional_predicates, new_goals)

    # print what the parser found
    print("updated parser")
    print('Types: ' + str(parser.types))
    print('Actions: ' + str(parser.actions))
    # loop through the actions
    for action in parser.actions:
        print(action)

    print('Predicates: ' + str(parser.predicates))
    print('Objects: ' + str(parser.objects))
    print('Positive goals: ' + str(parser.positive_goals))
    print('Negative goals: ' + str(parser.negative_goals))
    print('State: ' + str(parser.state))


    # solve
    print("\n\n Solution to Plan")
    planner = Planner()
    verbose = True

    # solve with updated parser
    plan = planner.solve_given_parser(parser)

    if plan is not None:
        print('plan:')
        for act in plan:
            print(act if verbose else act.name + ' ' + ' '.join(act.parameters))
    else:
        print('No plan was found')

    # modify