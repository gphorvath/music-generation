using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;
using UnityEditor;

public class AudioRequest : EditorWindow
{
    public string SAVE_DIRECTORY = "Assets/Sound/Music/";
    public string API_URL = "http://127.0.0.1:8000/generate";
    public string PROMPT = "125bpm+320kbps+48khz+synthwave+retro";
    public int TOKENS = 512;

    [MenuItem("Window/Audio Request")]
    public static void ShowWindow()
    {
        GetWindow<AudioRequest>("Audio Request");
    }

    void OnGUI()
    {
        SAVE_DIRECTORY = EditorGUILayout.TextField("Save Directory", SAVE_DIRECTORY);
        API_URL = EditorGUILayout.TextField("API URL", API_URL);
        PROMPT = EditorGUILayout.TextField("Prompt", PROMPT);
        TOKENS = EditorGUILayout.IntField("Tokens", TOKENS);

        if (GUILayout.Button("Generate Audio"))
        {
            GenerateAudio();
        }
    }

    void GenerateAudio()
    {
        string generate = "?prompt=" + PROMPT + "&tokens=" + TOKENS;

        WebClient client = new WebClient();
        byte[] response = client.DownloadData(API_URL + generate);

        string timestamp = System.DateTime.Now.ToString("yyyyMMddHHmmss");
        string path = SAVE_DIRECTORY + timestamp + ".wav";

        File.WriteAllBytes(path, response);
    }
}
