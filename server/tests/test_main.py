from fastapi.testclient import TestClient
import sys
  
# setting path - needed to get main
sys.path.append('..')

from ..main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() ==  {"Hello!": "This is a Trie API!"}

def test_post_method_add_word():
    """
    Tests adding a single word
    """
    response = client.post("/add-word/slingshot")
    assert response.status_code == 200
    assert response.json() == {"status": "slingshot added to Trie"}

def test_post_method_add_word2():
    """
    Tests adding two words
    """
    response = client.post("/add-word/slingshot is cool")
    assert response.status_code == 200
    assert response.json() == {"status": "slingshot is cool added to Trie"}

def test_delete_method_deleting_word_in_trie():
    """
    Tests deleting a word in the trie
    """
    #slingshot is already added in the trie per the test_post_method_add_word() function
    response = client.delete("/delete-word/slingshot")
    assert response.status_code == 200
    assert response.json() == {"status": "slingshot deleted from Trie"}

def test_delete_method_deleting_word_not_in_trie():
    """
    Tests deleting a word not in the trie
    """
    response = client.delete("/delete-word/sling")
    assert response.status_code == 200
    assert response.json() == {"status": "sling does not exist in Trie"}

def test_get_method_searching_word_in_trie():
    """
    Tests searching a word in the trie
    """
    client.post("/add-word/hello")
    response = client.get("/search/hello")
    assert response.status_code == 200
    assert response.json() == {"status": "hello found in Trie!"}

def test_get_method_searching_word_not_in_trie():
    """
    Tests searching a word not in the trie
    """
    response = client.get("/search/slingshot")       
    assert response.status_code == 200       
    #slingshot was deleted in an earlier test so it should not be in the trie anymore
    assert response.json() == {"status": "slingshot not found in Trie!"}

def test_get_method_suggestion():
    """
    Tests retrieving a list of suggestions in the Trie
    """
    client.post("/add-word/real madrid")
    client.post("/add-word/real bacon")
    client.post("/add-word/fake bacon")
    client.post("/add-word/real madrid")
    response = client.get("/suggestions/real")
    assert response.status_code == 200
    assert response.json() == ["real madrid", "real bacon"]

def test_get_method_suggestion_modified():
    """
    Tests retrieving a list of 3 suggestions in the Trie
    """
    client.post("/add-word/sli")
    client.post("/add-word/slingboy")
    client.post("/add-word/slinggirl")
    client.post("/add-word/slinggirl")
    client.post("/add-word/slingshot")
    response = client.get("/suggestions/sli?suggestion_nums=3")
    assert response.status_code == 200
    assert response.json() == ["slinggirl", "slingshot is cool","sli"]

def test_get_display():
    """
    Tests getting all the words
    """
    response = client.get("/display-trie")
    correct_all_words = ["real madrid", "slinggirl", "slingshot is cool", "hello", "real bacon", "fake bacon","sli", "slingboy", "slingshot"]
    assert response.status_code == 200
    assert response.json() == correct_all_words