#!/usr/bin/env python
# coding: utf-8


import os
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, List, Optional

"""Problem: Colors 51 states of USA in such a way that no two neighbouring states have the same color"""

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type

def inv_sort():
    global invcount
    invcount += 1

# Base class for all constraints
# Constraints are the pair of states, for example (Queensland, New South Wales)
class Constraint(Generic[V, D], ABC):
     # The variables that the constraint is between
    def __init__(self, variables: List[V]) -> None:
         self.variables = variables
  
     # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


# This is the Class for Constraints satisfaction problem, that is implemented using Backtraking
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables # variables to be constrained
        self.domains: Dict[V, List[D]] = domains # domain of each variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")
                
    #fuction to add a new constraint to the problem
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                 raise LookupError("Variable in constraint not in CSP")
            else:
                 self.constraints[variable].append(constraint)
                
    #Function to test if the new coloring decision is consistent or not                
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:

            """YOUR CODE STARTS HERE"""
            if not (constraint.satisfied(assignment)):
                return False
        return True
            

        raise NotImplementedError("Function CSP.consistent NOT IMPLEMENTED")



        """YOUR CODE ENDS HERE"""

    #Informed search backtracking implementation
    def backtracking_search(self,assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        """assignment is complete if every variable is assigned (our base case)"""
        if len(assignment) == len(self.variables):
            return assignment

        """YOUR CODE STARTS HERE"""
        """get all variables in the CSP but not in the assignment"""
        uncoloredStates : List[V] = []
        for variable in variables:
            if variable not in assignment:
                uncoloredStates.append(variable)

        """get the every possible domain value of the first unassigned variable"""
        currentState: V  = uncoloredStates[0]
        for color in self.domains[currentState]:
            assignment[currentState] = color
            """if we're still consistent, we recurse (continue)"""
            if self.consistent(currentState, assignment):
                coloredStates: Optional[Dict[V, D]] = self.backtracking_search(assignment) 
                if coloredStates is not None:
                    return coloredStates
        """if we didn't find the result, we will end up backtracking"""
        assignment.pop(currentState)
        return None 
        """YOUR CODE ENDS HERE"""
        raise NotImplementedError("Function CSP.backtracking_search NOT IMPLEMENTED")


class MapColoringConstraint(Constraint[str, str]):
     def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2
  
     def satisfied(self, assignment: Dict[str, str]) -> bool:

        """YOUR CODE STARTS HERE"""
        """If either place is not in the assignment then it is not
          yet possible for their colors to be conflicting"""
        if self.place1 not in assignment or self.place2 not in assignment:
            return True


        """check the color assigned to place1 is not the same as the
          color assigned to place2"""
        if not (assignment[self.place1] == assignment[self.place2]):
            return True
        return False


        """YOUR CODE ENDS HERE"""
        raise NotImplementedError("Function MapColoringConstraint.satisfied NOT IMPLEMENTED")
def plot(solution):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())

    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',
                                         category='cultural', name=shapename)

    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)

    ax.set_title('USA Map Coloring')

    # for state in shpreader.Reader(states_shp).geometries():
    for astate in shpreader.Reader(states_shp).records():
        edgecolor = 'black'

        facecolor = solution[astate.attributes['name']]

        ax.add_geometries([astate.geometry], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor=edgecolor)
    if not os.path.exists("mapColoring"):
        os.mkdir("mapColoring")
    plt.savefig(os.path.join("mapColoring", "map.png"))
    plt.show()


if __name__ == "__main__":
    invcount = 0


    abb = {
        "AL": "Alabama",
        "AK": "Alaska",
    #     "AS": "American Samoa",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "DC": "District of Columbia",
    #     "FM": "Federated States Of Micronesia",
        "FL": "Florida",
        "GA": "Georgia",
    #     "GU": "Guam",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
    #     "MH": "Marshall Islands",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
    #     "MP": "Northern Mariana Islands",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
    #     "PW": "Palau",
        "PA": "Pennsylvania",
    #     "PR": "Puerto Rico",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
    #     "VI": "Virgin Islands",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming"
    }
    path = 'res'

    neighbors = pd.read_csv(os.path.join(path, "neighbors-states.csv"))
    usa_states = [abb[i] for i in abb.keys()]

    color_list = ["red", "yellow", "green", "blue"]

    variables: List[str] = usa_states
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = color_list
    print(len(variables)**len(color_list))

    csp: CSP[str, str] = CSP(variables, domains)
    for i in range(111):
        a = neighbors["StateCode"][i]
        n = neighbors["NeighborStateCode"][i]
        if a in abb.keys() and n in abb.keys():
            csp.add_constraint(MapColoringConstraint(abb[a], abb[n]))

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:

        print(solution)

    plot(solution)

