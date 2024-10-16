import unittest
from unittest.mock import patch, MagicMock
from app import load_albums_with_band

class TestApp(unittest.TestCase):

    @patch('app.sqlite3.connect')
    def test_load_albums_with_band(self, mock_connect):
        # Configurer le mock pour la connexion SQLite
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Configurer le mock pour les résultats de la requête
        mock_cursor.fetchall.return_value = [
            ('Album1', 'Band1'),
            ('Album2', 'Band2')
        ]
        
        # Appeler la fonction
        result = load_albums_with_band()
        
        # Vérifier le résultat
        self.assertEqual(result, [('Album1', 'Band1'), ('Album2', 'Band2')])
        
        # Vérifier que les appels à la base de données ont été effectués correctement
        mock_connect.assert_called_once_with('music.db')
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('''SELECT a.title, b.name FROM Album a JOIN Band b ON a.band_id = b.id''')
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()