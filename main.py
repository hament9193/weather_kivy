import json
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

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
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        self.search_results.item_strings = cities

class WeatherRoot(BoxLayout):
    pass

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()