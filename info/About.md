# About

Markdown document dedicated to some design choices of the application.

## ConwaysGameOfLife

### Engine and Widget

The game itself is separated into 2 components - Engine and Widget.

Engine handles core logic and 2D board representation of the game.
For the engine, 2D board representation is stored internally 
using numpy array of characters representing cell state for each array element.
Externally, 2D board can be accessed by - row, column indexes for specific cell 
or as a python list converted from numpy array.

Moving onto the Widget.  
Widget creates an engine instance upon initialization and uses it to access core game elements to
render the widget and handle its geometry.
The other important part of actually running the game is to be able to handle its turn cycle.
It is achieved with connecting QTimer object to the engine's 'make_turn' method, so that after certain amount
of time the game would invoke it and evolve the game to the next turn.
Widget is responsible to handle some of engine's signals by connecting them to 
existing slots or creating specific handlers for them. 
Good example of such use is implementation of 'active cell' which acts like an extra method of input
that user can use to modify the game's state. In order to prevent edge cases where 'active cell' cursor can go off-field, '_handle_board_changes' method used to handle engine's 'board_changed' signal to prevent such  behavior.
Other method of input handles mouse events and directly interacts with engine's methods to apply the changes
the user intended to do.  
To wrap up, widget is responsible to handle some of engine's signals, rendering of the game and
keeping track of the turn cycle with a QTimer.

Engine and Widget classes have implementation and conceptual similarities.
First off, they both inherit from abc classes that are used to create interface to indicate that the class can safely be used with
'ConwaysGameOfLifeConfigManager' (Config Manager) and 'ConwaysGameOfLifePropertiesManager' (Properties Manager).  
Then there are similarities between Model-View and Engine-Widget approaches.
Engine acts as a model, providing information to the view.
While Widget communicates with the model  to obtain information from it and display it to the user!


### ABCs

`class MySerializable(ABC)` is used to ensure the `savable_properties_names` method is implemented. It is used
to obtain properties that are essential If the widget's configuration is intended to be saved into JSON format.

`class MyPropertySignalAccessor(ABC)` is used to ensure the `get_property_changed_signal` method is implemented.
The story with this is quite different. 
The `QtCore.Property` class, which is the Qt equivalent to python's `property` accepts `notify` keyword argument,
but has NO WAY of obtaining it back from thee `Property` object.
So the `get_property_changed_signal` method is used to obtain such signals.
Mostly it is implemented by enforcing fixed name convention for all the notify signals.

```python
_SIGNAL_SUFFIX = "_changed"

def get_property_changed_signal(self, name: str) -> Signal:
    name += self._SIGNAL_SUFFIX
    if isinstance(signal := getattr(self, name, None), Signal):
        return signal
    raise ValueError
```

Then to please the Qt Meta Object system, there is an annual game called 'Figure out how metaclasses work'.
After clearing it, the problem with inheritance and metaclasses should be resolved:

```python
class _MyMeta(type(QObject), ABCMeta):
    pass


class ConwaysGameOfLifeEngine(QObject, MySerializable, MyPropertySignalAccessor, metaclass=_MyMeta):
    ...
```

## Config Manager

Config Manager uses defined `deserialize_property` and `serialize_property` 
which are created MANUALLY (seriously why, +1 for custom conversion) to convert values between JSON and properties.

## Properties Manager

The Properties Manager requires more complex approach in order to handle read only properties, 
properties without notify signal and so on.
To convert property and set it to the widget value,
ANOTHER manual conversion needs to be done (+1 for custom conversion).
And to convert widget value to property supported value
ANOTHER ONE (+1 for custom conversion) have to be done.

### Dynamic Slot Creation

Speaking of connecting the notify signals to the dynamically created slots,
strange approach was taken... (no other was discovered)
1. Create `SlotFactory(QObject)` class (assign parent or keep at least one reference to the object (not sure about this, hehe...))
2. Create desired slot methods
3. Return the slot as `MethodType` object like this:
```python
def get_slot(self, property_name: str):
    method = self.SLOTS[property_name]
    bound_method = MethodType(method, self)
    return bound_method
```

Looking at all this crap and nonsense I would be glad If there exists a better solution.
But that works, so who cares.


## Main Widget

There is much dynamic and flexible design was done to this point,
so the main widget can relax and just take it easy.
Use available methods and classes to easily connect one object to another in the desired way, 
essentially act like a controller between objects connecting them to each other using some mediate method or function.

## Outro

Project seems to be almost logically complete, so would work on it some more and maybe try
to get some feedback, but afraid to do so, I am probably wasted.
