using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class TextAllocator : MonoBehaviour {

    private string text = "Hello World";
    private double delay = 0.1d;
    private int currentPosition = 0;

    public GameObject LyricsContainer;

    public List<GameObject> characters;
    public List<float> positions;

	// Use this for initialization
	void Start () {
        characters = new List<GameObject>();

        GameObject template = GameObject.Find("LyricsTemplate");
        GameObject camera = GameObject.Find("Camera");

        template.SetActive(false);


        foreach (char c in text)
        {
            GameObject p = (GameObject)Instantiate(template);
            characters.Add(p);
            p.GetComponent<TextMesh>().text = char.ToString(c);
            
        }

	}
	
	// Update is called once per frame
	void Update () {
	}
}
