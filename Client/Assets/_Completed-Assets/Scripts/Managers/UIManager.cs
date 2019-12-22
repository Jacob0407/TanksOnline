using UnityEngine;
using UnityEditor;

public class UIManager : Singleton<UIManager>
{
    [HideInInspector]
    public UIObjectManager m_uiObjectMgr;

    private int m_cacheMatchNum = 0;

    public void Start()
    {
        reginsterAllEvents();
    }

    public void Update()
    {
        if (m_cacheMatchNum > 0)
        {
            OnMatchNumChange(m_cacheMatchNum);
        }
    }

    public void reginsterAllEvents()
    {
        KBEngine.Event.registerOut("OnMatchNumChange", this, "OnMatchNumChange");
    }

    /// <summary>
    /// 相关数据重置
    /// </summary>
    public void resetData()
    {
        var gameObj = GameObject.Find("UIObjectManager") as GameObject;
        if (!gameObj)
            return;

        m_uiObjectMgr = gameObj.GetComponent<UIObjectManager>();
    }

    /// <summary>
    /// 登录按钮触发事件
    /// </summary>
    public void OnLoginClick()
    {
        if (m_uiObjectMgr == null)
            resetData();

        m_uiObjectMgr.loginClick();
    }

    /// <summary>
    /// 更新匹配玩家的人数
    /// </summary>
    /// <param name="curNum"></param>
    public void OnMatchNumChange(int curNum)
    {
        if (m_uiObjectMgr == null)
            resetData();

        string playerNum = curNum + "/" + 2;
        if (!m_uiObjectMgr.showMatchInfo(playerNum))
            m_cacheMatchNum = curNum;
        else
            m_cacheMatchNum = 0;
    }
}