"""Implement Environments (Chapters 1-2).

The class hierarchies are as follows:

Environment ## An environment holds objects, runs simulations
    XYEnvironment
        GridEnvironment
        ...

An agent program is a callable instance, taking percepts and choosing actions
    SimpleReflexAgentProgram
    ...

EnvGUI ## A window with a graphical representation of the Environment
EnvCanvas ## Canvas to display the environment of an EnvGUI

"""

# TO DO:
# Speed control in GUI does not have any effect -- fix it.

from .utils import distance_squared, turn_heading
from statistics import mean

import random
import copy
import collections

try:
    from ipythonblocks import BlockGrid
    from IPython.display import HTML, display
    from time import sleep
except:
    pass


# ______________________________________________________________________________



class Environment:
    """Abstract class representing an Environment. 'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .things and .agents (which is a subset
    of .things). Each agent has a .performance slot, initialized to 0.
    Each thing has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  # List of classes that can go into environment

    def percept(self, agent):
        """Return the percept that the agent sees at this point. (Implement this.)"""
        raise NotImplementedError

    def execute_action(self, agent, action):
        """Change the world to reflect this action. (Implement this.)"""
        raise NotImplementedError

    def default_location(self, thing):
        """Default location to place a new thing with unspecified location."""
        return None

    def exogenous_change(self):
        """If there is spontaneous change in the world, override this."""
        pass

    def is_done(self):
        """By default, we're done when we can't find a live agent."""
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()

    def run(self, steps=1000):
        """Run the Environment for given number of time steps."""
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def list_things_at(self, location, tclass=Thing):
        """Return all things exactly at a given location."""
        return [thing for thing in self.things
                if thing.location == location and isinstance(thing, tclass)]

    def some_things_at(self, location, tclass=Thing):
        """Return true if at least one of the things at location
        is an instance of class tclass (or a subclass)."""
        return self.list_things_at(location, tclass) != []

    def add_thing(self, thing, location=None):
        """Add a thing to the environment, setting its location. For
        convenience, if thing is an agent program we make a new agent
        for it. (Shouldn't need to override this.)"""
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        if thing in self.things:
            print("Can't add the same thing twice")
        else:
            thing.location = location if location is not None else self.default_location(thing)
            self.things.append(thing)
            if isinstance(thing, Agent):
                thing.performance = 0
                self.agents.append(thing)

    def delete_thing(self, thing):
        """Remove a thing from the environment."""
        try:
            self.things.remove(thing)
        except ValueError as e:
            print(e)
            print("  in Environment delete_thing")
            print("  Thing to be removed: {} at {}".format(thing, thing.location))
            print("  from list: {}".format([(thing, thing.location) for thing in self.things]))
        if thing in self.agents:
            self.agents.remove(thing)



class XYEnvironment(Environment):
    """This class is for environments on a 2D plane, with locations
    labelled by (x, y) points, either discrete or continuous.

    Agents perceive things within a radius. Each agent in the
    environment has a .location slot which should be a location such
    as (0, 1), and a .holding slot, which should be a list of things
    that are held."""

    def __init__(self, width=10, height=10):
        super().__init__()

        self.width = width
        self.height = height
        self.observers = []
        # Sets iteration start and end (no walls).
        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width, self.height)

    perceptible_distance = 1

    def things_near(self, location, radius=None):
        """Return all things within radius of location."""
        if radius is None:
            radius = self.perceptible_distance
        radius2 = radius * radius
        return [(thing, radius2 - distance_squared(location, thing.location))
                for thing in self.things if distance_squared(
                                                location, thing.location) <= radius2]

    def percept(self, agent):
        """By default, agent perceives things within a default radius."""
        return self.things_near(agent.location)

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'TurnRight':
            agent.direction += Direction.R
        elif action == 'TurnLeft':
            agent.direction += Direction.L
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
#         elif action == 'Grab':
#             things = [thing for thing in self.list_things_at(agent.location)
#                     if agent.can_grab(thing)]
#             if things:
#                 agent.holding.append(things[0])
        elif action == 'Release':
            if agent.holding:
                agent.holding.pop()

    def default_location(self, thing):
        return (random.choice(self.width), random.choice(self.height))

    def move_to(self, thing, destination):
        """Move a thing to a new location. Returns True on success or False if there is an Obstacle.
        If thing is holding anything, they move with him."""
        thing.bump = self.some_things_at(destination, Obstacle)
        if not thing.bump:
            thing.location = destination
            for o in self.observers:
                o.thing_moved(thing)
            for t in thing.holding:
                self.delete_thing(t)
                self.add_thing(t, destination)
                t.location = destination
        return thing.bump

    def add_thing(self, thing, location=(1, 1), exclude_duplicate_class_items=False):
        """Adds things to the world. If (exclude_duplicate_class_items) then the item won't be
        added if the location has at least one item of the same class."""
        if (self.is_inbounds(location)):
            if (exclude_duplicate_class_items and
                    any(isinstance(t, thing.__class__) for t in self.list_things_at(location))):
                return
            super().add_thing(thing, location)

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds (within walls if we have walls)"""
        x, y = location
        return not (x < self.x_start or x >= self.x_end or y < self.y_start or y >= self.y_end)

    def random_location_inbounds(self, exclude=None):
        """Returns a random location that is inbounds (within walls if we have walls)"""
        location = (random.randint(self.x_start, self.x_end),
                    random.randint(self.y_start, self.y_end))
        if exclude is not None:
            while(location == exclude):
                location = (random.randint(self.x_start, self.x_end),
                            random.randint(self.y_start, self.y_end))
        return location

    def delete_thing(self, thing):
        """Deletes thing, and everything it is holding (if thing is an agent)"""
        if isinstance(thing, Agent):
            for obj in thing.holding:
                super().delete_thing(obj)
                for obs in self.observers:
                    obs.thing_deleted(obj)

        super().delete_thing(thing)
        for obs in self.observers:
            obs.thing_deleted(thing)

    def add_walls(self):
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width):
            self.add_thing(Wall(), (x, 0))
            self.add_thing(Wall(), (x, self.height - 1))
        for y in range(self.height):
            self.add_thing(Wall(), (0, y))
            self.add_thing(Wall(), (self.width - 1, y))

        # Updates iteration start and end (with walls).
        self.x_start, self.y_start = (1, 1)
        self.x_end, self.y_end = (self.width - 1, self.height - 1)

    def add_observer(self, observer):
        """Adds an observer to the list of observers.
        An observer is typically an EnvGUI.

        Each observer is notified of changes in move_to and add_thing,
        by calling the observer's methods thing_moved(thing)
        and thing_added(thing, loc)."""
        self.observers.append(observer)

    def turn_heading(self, heading, inc):
        """Return the heading to the left (inc=+1) or right (inc=-1) of heading."""
        return turn_heading(heading, inc)


class Obstacle(Thing):
    """Something that can cause a bump, preventing an agent from
    moving into the same square it's in."""
    pass


class Wall(Obstacle):
    pass

# ______________________________________________________________________________



class GraphicEnvironment(XYEnvironment):
    def __init__(self, width=10, height=10, boundary=True, color={}, display=False):
        """Define all the usual XYEnvironment characteristics,
        but initialise a BlockGrid for GUI too."""
        super().__init__(width, height)
        self.grid = BlockGrid(width, height, fill=(200, 200, 200))
        if display:
            self.grid.show()
            self.visible = True
        else:
            self.visible = False
        self.bounded = boundary
        self.colors = color

    def get_world(self):
        """Returns all the items in the world in a format
        understandable by the ipythonblocks BlockGrid."""
        result = []
        x_start, y_start = (0, 0)
        x_end, y_end = self.width, self.height
        for x in range(x_start, x_end):
            row = []
            for y in range(y_start, y_end):
                row.append(self.list_things_at([x, y]))
            result.append(row)
        return result

    """
    def run(self, steps=1000, delay=1):
        "" "Run the Environment for given number of time steps,
        but update the GUI too." ""
        for step in range(steps):
            sleep(delay)
            if self.visible:
                self.reveal()
            if self.is_done():
                if self.visible:
                    self.reveal()
                return
            self.step()
        if self.visible:
            self.reveal()
    """

    def run(self, steps=1000, delay=1):
        """Run the Environment for given number of time steps,
        but update the GUI too."""
        for step in range(steps):
            self.update(delay)
            if self.is_done():
                break
            self.step()
        self.update(delay)

    def update(self, delay=1):
        sleep(delay)
        if self.visible:
            self.conceal()
            self.reveal()
        else:
            self.reveal()

    def reveal(self):
        """Display the BlockGrid for this world - the last thing to be added
        at a location defines the location color."""
        self.draw_world()
        self.grid.show()
        self.visible = True

    def draw_world(self):
        self.grid[:] = (200, 200, 200)
        world = self.get_world()
        for x in range(0, len(world)):
            for y in range(0, len(world[x])):
                if len(world[x][y]):
                    self.grid[y, x] = self.colors[world[x][y][-1].__class__.__name__]

    def conceal(self):
        """Hide the BlockGrid for this world"""
        self.visible = False
        display(HTML(''))


class WumpusEnvironment(XYEnvironment):
    pit_probability = 0.2  # Probability to spawn a pit in a location. (From Chapter 7.2)
    # Room should be 4x4 grid of rooms. The extra 2 for walls

    def __init__(self, agent_program, width=6, height=6):
        super().__init__(width, height)
        self.init_world(agent_program)

    def init_world(self, program):
        """Spawn items in the world based on probabilities from the book"""

        "WALLS"
        self.add_walls()

        "PITS"
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                if random.random() < self.pit_probability:
                    self.add_thing(Pit(), (x, y), True)
                    self.add_thing(Breeze(), (x - 1, y), True)
                    self.add_thing(Breeze(), (x, y - 1), True)
                    self.add_thing(Breeze(), (x + 1, y), True)
                    self.add_thing(Breeze(), (x, y + 1), True)

        "WUMPUS"
        w_x, w_y = self.random_location_inbounds(exclude=(1, 1))
        self.add_thing(Wumpus(lambda x: ""), (w_x, w_y), True)
        self.add_thing(Stench(), (w_x - 1, w_y), True)
        self.add_thing(Stench(), (w_x + 1, w_y), True)
        self.add_thing(Stench(), (w_x, w_y - 1), True)
        self.add_thing(Stench(), (w_x, w_y + 1), True)

        "GOLD"
        self.add_thing(Gold(), self.random_location_inbounds(exclude=(1, 1)), True)

        "AGENT"
        self.add_thing(Explorer(program), (1, 1), True)

    def get_world(self, show_walls=True):
        """Returns the items in the world"""
        result = []
        x_start, y_start = (0, 0) if show_walls else (1, 1)

        if show_walls:
            x_end, y_end = self.width, self.height
        else:
            x_end, y_end = self.width - 1, self.height - 1

        for x in range(x_start, x_end):
            row = []
            for y in range(y_start, y_end):
                row.append(self.list_things_at((x, y)))
            result.append(row)
        return result

    def percepts_from(self, agent, location, tclass=Thing):
        """Returns percepts from a given location,
        and replaces some items with percepts from chapter 7."""
        thing_percepts = {
            Gold: Glitter(),
            Wall: Bump(),
            Wumpus: Stench(),
            Pit: Breeze()}

        """Agents don't need to get their percepts"""
        thing_percepts[agent.__class__] = None

        """Gold only glitters in its cell"""
        if location != agent.location:
            thing_percepts[Gold] = None

        result = [thing_percepts.get(thing.__class__, thing) for thing in self.things
                  if thing.location == location and isinstance(thing, tclass)]
        return result if len(result) else [None]

    def percept(self, agent):
        """Returns things in adjacent (not diagonal) cells of the agent.
        Result format: [Left, Right, Up, Down, Center / Current location]"""
        x, y = agent.location
        result = []
        result.append(self.percepts_from(agent, (x - 1, y)))
        result.append(self.percepts_from(agent, (x + 1, y)))
        result.append(self.percepts_from(agent, (x, y - 1)))
        result.append(self.percepts_from(agent, (x, y + 1)))
        result.append(self.percepts_from(agent, (x, y)))

        """The wumpus gives out a loud scream once it's killed."""
        wumpus = [thing for thing in self.things if isinstance(thing, Wumpus)]
        if len(wumpus) and not wumpus[0].alive and not wumpus[0].screamed:
            result[-1].append(Scream())
            wumpus[0].screamed = True

        return result

    def execute_action(self, agent, action):
        """Modify the state of the environment based on the agent's actions.
        Performance score taken directly out of the book."""

        if isinstance(agent, Explorer) and self.in_danger(agent):
            return

        agent.bump = False
        if action == 'TurnRight':
            agent.direction += Direction.R
            agent.performance -= 1
        elif action == 'TurnLeft':
            agent.direction += Direction.L
            agent.performance -= 1
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
            agent.performance -= 1
        elif action == 'Grab':
            things = [thing for thing in self.list_things_at(agent.location)
                      if agent.can_grab(thing)]
            if len(things):
                print("Grabbing", things[0].__class__.__name__)
                if len(things):
                    agent.holding.append(things[0])
            agent.performance -= 1
        elif action == 'Climb':
            if agent.location == (1, 1):  # Agent can only climb out of (1,1)
                agent.performance += 1000 if Gold() in agent.holding else 0
                self.delete_thing(agent)
        elif action == 'Shoot':
            """The arrow travels straight down the path the agent is facing"""
            if agent.has_arrow:
                arrow_travel = agent.direction.move_forward(agent.location)
                while(self.is_inbounds(arrow_travel)):
                    wumpus = [thing for thing in self.list_things_at(arrow_travel)
                              if isinstance(thing, Wumpus)]
                    if len(wumpus):
                        wumpus[0].alive = False
                        break
                    arrow_travel = agent.direction.move_forward(agent.location)
                agent.has_arrow = False

    def in_danger(self, agent):
        """Checks if Explorer is in danger (Pit or Wumpus), if he is, kill him"""
        for thing in self.list_things_at(agent.location):
            if isinstance(thing, Pit) or (isinstance(thing, Wumpus) and thing.alive):
                agent.alive = False
                agent.performance -= 1000
                agent.killed_by = thing.__class__.__name__
                return True
        return False

    def is_done(self):
        """The game is over when the Explorer is killed
        or if he climbs out of the cave only at (1,1)."""
        explorer = [agent for agent in self.agents if isinstance(agent, Explorer)]
        if len(explorer):
            if explorer[0].alive:
                return False
            else:
                print("Death by {} [-1000].".format(explorer[0].killed_by))
        else:
            print("Explorer climbed out {}."
                  .format(
                      "with Gold [+1000]!" if Gold() not in self.things else "without Gold [+0]"))
        return True


