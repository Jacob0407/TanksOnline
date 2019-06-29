using KBEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIEventControl : MonoBehaviour
{
    public GameObject loginAccount;
    public GameObject loginPwd;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    /// <summary>
    /// 登录按钮触发事件
    /// </summary>
    public void OnLoginClick()
    {
        if (loginAccount == null || loginPwd == null)
        {
            Debug.LogError("loginAccount or loginPwd is null");
            return;
        }

        string account = loginAccount.GetComponent<InputField>().text;
        string pwd = loginPwd.GetComponent<InputField>().text;

        if (account.Length <= 3 || pwd.Length <= 3)
        {
            Debug.LogError("account or pwd invalid");
            return;
        }

        Debug.Log("login, account: " + account + "pwd: " + pwd);

        KBEngineApp.app.login(account, pwd, System.Text.Encoding.UTF8.GetBytes("kbengine_unity3d_demo"));
    }
}
