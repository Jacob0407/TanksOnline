using UnityEngine;
using UnityEditor;

public class UIEventHandler : MonoBehaviour
{
    public void OnLoginClick()
    {
        UIManager.Instance.OnLoginClick();
    }
}