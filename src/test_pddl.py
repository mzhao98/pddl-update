from pddl_parser.planner import PDDL_Parser, Planner
from pddl_parser.action import Action

domain = 'serving_domain/domain.pddl'
problem = 'serving_domain/problem.pddl'
parser = PDDL_Parser()
print('----------------------------')
print(parser.scan_tokens(domain))
print('----------------------------')
print(parser.scan_tokens(problem))
print('----------------------------')
parser.parse_domain(domain)
parser.parse_problem(problem)
print('Domain name: ' + str(parser.domain_name))

# print what the parser found
print('Types: ' + str(parser.types))
print('Actions: ' + str(parser.actions))
print('Predicates: ' + str(parser.predicates))
print('Objects: ' + str(parser.objects))
print('Positive goals: ' + str(parser.positive_goals))
print('Negative goals: ' + str(parser.negative_goals))
print('State: ' + str(parser.state))

# write a function to update the actions by adding a new capability
def add_capability(action, capability):
    new_action = Action(action.name, action.parameters, action.positive_preconditions, action.negative_preconditions,
                        action.add_effects, action.del_effects)
    return new_action

# update the actions
new_action = '''(:action read-aloud-recipe
        :parameters (?rob - robot ?rec - recipe)
        :effect (recipe-announced recipe1)
    )'''
# update the actions of the parser
# convert new_action to Action class, read from above
new_action = Action('read-aloud-recipe', [['?rob', 'robot'],[ '?rec', 'recipe']], [], [],  [('recipe-announced','rec')], [])
parser.actions.append(new_action)

# update the goal to have the new constraint that the recipe must be announced
parser.positive_goals.add(('recipe-announced', 'recipe1'))

# print what the parser found
print("updated parser")
print('Types: ' + str(parser.types))
print('Actions: ' + str(parser.actions))
print('Predicates: ' + str(parser.predicates))
print('Objects: ' + str(parser.objects))
print('Positive goals: ' + str(parser.positive_goals))
print('Negative goals: ' + str(parser.negative_goals))
print('State: ' + str(parser.state))


# solve
print("\n\n Solution to Plan")
planner = Planner()
verbose = True

# print the actions
# plan = planner.solve(domain, problem)
# solve with updated parser
plan = planner.solve_given_parser(parser)

if plan is not None:
    print('plan:')
    for act in plan:
        print(act if verbose else act.name + ' ' + ' '.join(act.parameters))
else:
    print('No plan was found')

# modify