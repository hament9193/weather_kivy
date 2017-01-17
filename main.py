import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
# factory is to get instance of dynamic class (i.e. class cerated without declaration)
# widget for dynamic class is made with @ notation
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty

token = "bb233f234bc3eb3df4ecb30859da8d9e"
class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/" + \
                          "find?q={}&type=like&APPID=" + token
        search_url = search_template.format(self.search_input.text)
        request = UrlRequest(search_url, self.found_location)

    """
    found location will be triggered after getting response from url request.
    """
    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        if data and 'list' in data:
            cities = [(d['name'], d['sys']['country']) for d in data['list']]
            # cities = ["{} ({})".format(d['name'], d['sys']['country'])
            #           for d in data['list']]
            self.search_results.item_strings = cities
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results.adapter.data.extend(cities)
            self.search_results._trigger_reset_populate()
        else:
            del self.search_results.adapter.data[:]
            # self.search_results.adapter.data.clear() #introduced in python3
            self.search_results._trigger_reset_populate()

        """ custom function called args_converter.This function should accept two values: the index of the item being rendered,
        and the item itself.Kivy will call this function repeatedly for each item in the underlying data list
        NEED to set arg converter for adapter in kv file"""
    def args_converter(self, index, data_item):
        city, country = data_item
        return {'location': (city, country)}

class LocationButton(ListItemButton):
    location = ListProperty()


class CurrentWeather(BoxLayout):
    location = ListProperty(['New York', 'US'])
    conditions = ObjectProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        weather_template = "http://api.openweathermap.org/data/2.5/" +\
                           "weather?q={},{}&units=metric&APPID=" + token
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.render_conditions(data['weather'][0]['description'])
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']

    def render_conditions(self, conditions_description):
        if "clear" in conditions_description.lower():
            conditions_widget = Factory.ClearConditions()
        elif "rain" in conditions_description.lower():
            conditions_widget = RainConditions()
        elif "snow" in conditions_description.lower():
            conditions_widget = SnowConditions()
        else:
            conditions_widget = Factory.UnknownConditions()
        conditions_widget.conditions = conditions_description
        self.conditions.clear_widgets()
        self.conditions.add_widget(conditions_widget)

class Conditions(BoxLayout):
    conditions = StringProperty()

class SnowConditions(Conditions):
    FLAKE_SIZE = 5
    NUM_FLAKES = 60
    FLAKE_AREA = FLAKE_SIZE * NUM_FLAKES
    FLAKE_INTERVAL = 1.0 / 30.0
    def __init__(self, **kwargs):
        super(SnowConditions, self).__init__(**kwargs)
        self.flakes = [[x * self.FLAKE_SIZE, 0] for x in range(self.NUM_FLAKES)]
        Clock.schedule_interval(self.update_flakes, self.FLAKE_INTERVAL)
    def update_flakes(self, time):
        for f in self.flakes:
            f[0] += random.choice([-1, 1])
            f[1] -= random.randint(0, self.FLAKE_SIZE)
            if f[1] <= 0:
                f[1] = random.randint(0, int(self.height))
        self.canvas.before.clear()
        with self.canvas.before:
            widget_x = self.center_x - self. FLAKE_AREA / 2
            widget_y = self.pos[1]
            for x_flake, y_flake in self.flakes:
                x = widget_x + x_flake
                y = widget_y + y_flake
                Color(0.9, 0.9, 1.0)
                Ellipse(pos=(x, y), size=(self.FLAKE_SIZE, self.FLAKE_SIZE))

class RainConditions(Conditions):
    DROP_SIZE = 4
    NUM_DROPS = 30
    DROP_AREA = DROP_SIZE * NUM_DROPS*3
    DROP_INTERVAL = 1.0 / 10.0
    def __init__(self, **kwargs):
        super(RainConditions, self).__init__(**kwargs)
        self.drops = [[3 * x * self.DROP_SIZE, 0] for x in range(self.NUM_DROPS)]
        Clock.schedule_interval(self.update_drops, self.DROP_INTERVAL)

    def update_drops(self, time):
        for f in self.drops:
            f[1] = random.randint(0, self.DROP_SIZE)
        self.canvas.before.clear()
        with self.canvas.before:
            widget_x = self.center_x - self.DROP_AREA/2
            widget_y = self.pos[1]
            for x_flake, y_flake in self.drops:
                x = widget_x + x_flake
                y = widget_y + y_flake
                Color(0.9, 0.9, 1.0)
                Ellipse(pos=(x, y), size=(self.DROP_SIZE, self.DROP_SIZE))
                while y < self.center_y+(self.DROP_AREA/3):
                    y += random.randint(self.DROP_SIZE*2,self.DROP_SIZE*4)
                    Color(0.9, 0.9, 1.0)
                    Ellipse(pos=(x, y), size=(self.DROP_SIZE, self.DROP_SIZE))

class WeatherRoot(BoxLayout):
    addlocation = ObjectProperty()
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):
        self.clear_widgets()
        if self.current_weather is None:
            self.current_weather = CurrentWeather()
        if location is not None:
            self.current_weather.location = location
        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(self.addlocation)

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()