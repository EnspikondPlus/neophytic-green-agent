from dataclasses import dataclass
from typing import Optional, List
from pydantic import Field
from enum import Enum
from openenv.core.env_server.types import Action, Observation, State

class Command(str, Enum):
    MOVE = "move"
    INSPECT = "inspect"
    USEKEY = "usekey"
    GETKEY = "getkey"
    COMMIT = "commit"

class RoomsAction(Action):
    command: Command
    target_room: Optional[int] = None

class RoomsObservation(Observation):
    current_room: int = Field(..., description="Agent's current room")
    committed: int = Field(..., description="If observation phase finished, 0 if not finished, 1 if finished")

    room_visited: List[int] = Field(
        ..., description="Which rooms have been visited, 0 if not visited, 1 if known"
    )

    room_inspected: List[int] = Field(
        ..., description="Which rooms have been inspected, 0 if not inspected, 1 if inspected"
    )

    room_known_connects: List[List[int]] = Field(
        ..., description="Observed room connections, 1 at index (i,j) means rooms i, j are connected"
    )

    room_locked: List[int] = Field(
        ..., description="Whether current room is locked, -1 if unknown, 0 if unlocked, 1 if locked"
    )

    room_haskey: List[int] = Field(
        ..., description="Whether current room contains a key, -1 if unknown, 0 if no key, 1 if key"
    )

    room_exit: List[int] = Field(
        ..., description="Whether current room is the exit, -1 if unknown, 0 if not exit, 1 if exit"
    )

    current_keys: int = Field(..., description="Keys currently held")
    steps_remaining: int = Field(..., description="Remaining step budget")
    obs_inspect_weight: float = Field(..., description="Cost of using inspect in observation phase")

    failure_last: int = Field(
        ..., description="Whether last action failed, -1 if unknown, 0 if not failure, 1 if failure"
    )

class RoomsState(State):
    # Episode bookkeeping
    episode_id: str
    step_count: int

    # Map structure
    room_included: List[int]         
    room_connections: List[List[int]]    
    room_locked: List[int]  
    room_haskey: List[int]         
    room_exit: List[int]     

    # Agent knowledge tracking (hidden)
    room_visited: List[int]
    room_inspected: List[int]

    # Agent status
    current_room: int 
    current_keys: int

    # Phase control
    committed: int  

    # Budgeting
    steps_remaining: int
    obs_inspect_weight: float
    weighted_steps_used: float

    # Failure handling
    failure_show: bool
    failure_consequence: bool
    failure_last: int

    commit_reset: bool
    encoding: str

    done: bool