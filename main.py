from prueba_data import MailTrackDataTest
import os

if __name__ == '__main__':
    if not os.path.exists('resultados'):
        os.mkdir('resultados')

    mt = MailTrackDataTest('datos/user_connections.csv', 
    					   'datos/users.csv', 
    					   'datos/countries.csv')

    mt.pregunta_1().to_csv('resultados/pregunta_1.csv', index=False)
    mt.pregunta_2().to_csv('resultados/pregunta_2.csv', index=False)
    mt.pregunta_3().to_csv('resultados/pregunta_3.csv', index=False)
    mt.pregunta_4().to_csv('resultados/pregunta_4.csv', index=False)
    mt.pregunta_5().to_csv('resultados/pregunta_5.csv', index=False)
