from geosolver.database.geoserver_interface import geoserver_interface

__author__ = 'minjoon'

def test_geoserver_interface():
    data = geoserver_interface.download_questions(1)
    print(data)


if __name__ == "__main__":
    test_geoserver_interface()