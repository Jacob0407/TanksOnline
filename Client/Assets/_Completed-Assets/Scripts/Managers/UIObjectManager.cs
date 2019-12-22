using UnityEngine;
using UnityEditor;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using KBEngine;

public class UIObjectManager : MonoBehaviour
{
    #region 登录界面相关UI组件
    public GameObject loginAccount;
    public GameObject loginPwd;
    #endregion

    #region 匹配界面相关UI组件
    public GameObject matchPlayerNum;
    #endregion

    public void Start()
    {
        UIManager.Instance.resetData();
    }

    public void loginClick()
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

    public bool showMatchInfo(string matchInfo)
    {
        if (matchPlayerNum == null)
            return false;

        matchPlayerNum.GetComponent<Text>().text = matchInfo;

        return true;
    }
}