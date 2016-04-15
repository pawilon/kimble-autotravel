import string
import copy

# Constants
FORM = "ID:j_id0:j_id1:TheForm"
WAIT_SECONDS = "2"
URL = "https://eu1.salesforce.com/a32/o"
REPLAYSPEED = "FAST"


class MacroField(object):
    # A convenience method with correct format for an attribute
    @staticmethod
    def _macro_attr_format(name, value):
        if value == '':
            return '{0}=""'.format(name)
        elif value is None:
            return ''
        else:
            return '{0}={1}'.format(name, value)

    def __str__(self):
        return repr(self)


class TagField(MacroField):
    _DEFAULT_POS = "1"
    _DEFAULT_TYPE = None
    _DEFAULT_FORM = FORM if FORM else None
    _DEFAULT_ATTR = None
    _DEFAULT_CONTENT = None
    ENTRY_TYPE = "TAG"

    @property
    def pos(self):
        return MacroField._macro_attr_format("POS", self._pos)

    @property
    def type(self):
        return MacroField._macro_attr_format("TYPE", self._type)

    @property
    def form(self):
        return MacroField._macro_attr_format("FORM", self._form)

    @property
    def attr(self):
        return MacroField._macro_attr_format("ATTR", self._attr)

    @property
    def content(self):
        if self._type != "SELECT":
            return MacroField._macro_attr_format("CONTENT", str(self._content).replace(' ', '<SP>').replace('\n', '<BR>') if self._content is not None else None)
        else:
            return MacroField._macro_attr_format("CONTENT", '%"{0}"'.format(self._content) if self._content is not None else None)

    @content.setter
    def content(self, value):
        self._content = value

    def __init__(self, pos=_DEFAULT_POS, type=_DEFAULT_TYPE, form=_DEFAULT_FORM, attr=_DEFAULT_ATTR, content=_DEFAULT_CONTENT):
        self._pos = pos
        self._type = type
        self._form = form
        self._attr = "{0}:{1}".format(form, attr) if form else attr
        self._content = content

    def __repr__(self):
        return string.join([self.ENTRY_TYPE, self.pos, self.type, self.form, self.attr, self.content], " ")


class WaitField(MacroField):
    entry_type = "WAIT"

    @property
    def seconds(self):
        return MacroField._macro_attr_format("SECONDS", self._seconds)

    def __init__(self, seconds=None):
        self._seconds = seconds

    def __repr__(self):
        return string.join([self.entry_type, self.seconds], " ")


class Param:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Generator:
    param_dict = {
        'global': [
            Param(None, 'VERSION BUILD=8961227 RECORDER=FX'),
            Param(None, 'TAB T=1'),
            Param(None, 'SET !REPLAYSPEED {0}'.format(REPLAYSPEED)),
            Param(None, 'URL GOTO={0}'.format(URL)),
            Param(None, 'TAG POS=1 TYPE=A ATTR=TXT:"Travel Requests"'),
            Param(None, 'TAG POS=1 TYPE=INPUT:BUTTON FORM=ID:hotlist ATTR=NAME:new'),
            Param('main_traveller', TagField(type='INPUT:TEXT', attr='j_id104:j_id108:j_id109:j_id112')),
            Param('travel_summary', TagField(type='INPUT:TEXT', attr='j_id104:j_id108:j_id117:j_id119')),
            Param('to_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id108:j_id125:j_id128')),
            Param('from_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id108:j_id120:j_id123')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('activity', TagField(type='SELECT', attr='j_id104:j_id108:j_id130:ActivityList')),
            Param('reason', TagField(type='TEXTAREA', attr='j_id104:j_id108:j_id138:j_id140')),
            Param('luggage', TagField(type='INPUT:CHECKBOX', attr='j_id104:j_id141:j_id142:0:j_id143'))
        ],
        'flights': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Flight"')),
            Param(None, WaitField(WAIT_SECONDS)),
            # Select one way only
            Param(None, TagField(type='INPUT:RADIO', attr='j_id104:j_id150:{0}:j_id164:0')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('departure_airport', TagField(type='SELECT', attr='j_id104:j_id150:{0}:j_id170')),
            Param('destination_airport', TagField(type='SELECT', attr='j_id104:j_id150:{0}:j_id172')),
            Param('departure_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id150:{0}:j_id174')),
            Param('departure_time', TagField(type='SELECT', attr='j_id104:j_id150:{0}:j_id176')),
            Param('requisition_notes', TagField(type='TEXTAREA', attr='j_id104:j_id150:{0}:j_id189'))
        ],
        'hotels': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Hotel"')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('check_in', TagField(type='INPUT:TEXT', attr='j_id104:j_id194:{0}:j_id207')),
            Param('check_out', TagField(type='INPUT:TEXT', attr='j_id104:j_id194:{0}:j_id210')),
            Param('preference', TagField(type='INPUT:TEXT', attr='j_id104:j_id194:{0}:j_id213')),
            Param('requisition_notes', TagField(type='TEXTAREA', attr='j_id104:j_id194:{0}:j_id216'))
        ],
        'trains': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Train"')),
            Param(None, WaitField(WAIT_SECONDS)),
            # Select one way only
            Param(None, TagField(type='INPUT:RADIO', attr='j_id104:j_id221:{0}:j_id235:0')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('departure_station', TagField(type='INPUT:TEXT', attr='j_id104:j_id221:{0}:j_id241')),
            Param('departure_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id221:{0}:j_id243')),
            Param('departure_time', TagField(type='SELECT', attr='j_id104:j_id221:{0}:j_id245')),
            Param('destination_station', TagField(type='INPUT:TEXT', attr='j_id104:j_id221:{0}:j_id250')),
            Param('requisition_notes', TagField(type='TEXTAREA', attr='j_id104:j_id221:{0}:j_id263'))
        ],
        'taxis': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Taxi"')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('departure_address', TagField(type='TEXTAREA', attr='j_id104:j_id268:{0}:j_id281')),
            Param('departure_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id268:{0}:j_id284')),
            Param('departure_time', TagField(type='INPUT:TEXT', attr='j_id104:j_id268:{0}:j_id287')),
            Param('destination_address', TagField(type='TEXTAREA', attr='j_id104:j_id268:{0}:j_id292')),
            Param('requisition_notes', TagField(type='TEXTAREA', attr='j_id104:j_id268:{0}:j_id297'))
        ],
        'cars': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Car Hire"')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('pickup', TagField(type='INPUT:TEXT', attr='j_id104:j_id302:{0}:j_id315')),
            Param('pickup_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id302:{0}:j_id318')),
            Param('dropoff', TagField(type='INPUT:TEXT', attr='j_id104:j_id302:{0}:j_id323')),
            Param('dropoff_date', TagField(type='INPUT:TEXT', attr='j_id104:j_id302:{0}:j_id326')),
            Param('requisition_notes', TagField(type='TEXTAREA', attr='j_id104:j_id302:{0}:j_id331'))
        ],
        'other_travellers': [
            Param(None, TagField(type='H2', form=None, attr='TXT:"Add Other Traveller"')),
            Param(None, WaitField(WAIT_SECONDS)),
            Param('name', TagField(type='INPUT:TEXT', attr='j_id104:j_id335:{0}:j_id341'))
        ]
    }

    def __init__(self, itinerary, url=URL):
        self.itinerary = itinerary
        self.url = url

    def generate(self):
        # Not using param_dict.keys(), as I want them to be in order
        keys = ['global', 'flights', 'hotels', 'trains', 'taxis', 'cars', 'other_travellers']
        output = []
        for key in keys:
            if key in self.itinerary:
                output.append("' {0}".format(key))
                # Global doesn't use an array of items, so has slightly different code
                if key == 'global':
                    for param in self.param_dict[key]:
                        if param.name is not None:
                            content = self.itinerary[key].get(param.name)
                            if content is not None:
                                value = copy.copy(param.value)
                                value.content = content
                                output.append(str(value))
                        else:
                            output.append(str(param.value))
                else:
                    item_counter = 0
                    for item in self.itinerary[key]:
                        for param in self.param_dict[key]:
                            if param.name is not None:
                                content = item.get(param.name)
                                if content is not None:
                                    value = copy.copy(param.value)
                                    value.content = content
                                    output.append(str(value).format(item_counter))
                            else:
                                output.append(str(param.value).format(item_counter))
                        item_counter += 1
                output.append('\n')
        return string.join(output, '\n')


def convert_to_imacro(itinerary, url=URL):
    generator = Generator(itinerary, url)
    return generator.generate()
