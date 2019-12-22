using UnityEngine;
using UnityEditor;
using KBEngine;
using UnityEngine.SceneManagement;
using Complete;

public class PlayerAvatar : PlayerAvatarBase
{
    public TankManager m_TankManager = new TankManager();   // 对于的实际控制坦克
    private bool firstMatch = true;

    public override void onEnter()
    {
        Dbg.INFO_MSG("PlayerAvatar::onEnter");
        this.baseEntityCall.reqMatch();
    }

    public override void onEnterWorld()
    {
        Dbg.INFO_MSG("EnterWorld, " + KBEngineApp.app.spaceID);
        if (this.isPlayer())
            GameManager.g_MainPlayer = this;
        else
            GameManager.g_OtherPlayers[this.id] = this;
    }

    public override void onEnterSpace()
    {
        Dbg.INFO_MSG("onEnterSpace, " + KBEngineApp.app.spaceID);
    }

    public override void enterBattleSpace(AVATAR_INFO_LIST allAvatarInfo)
    {
        Dbg.INFO_MSG("PlayerAvatar::enterBattleSpace");
        GameManager.SetAllAvatarBaseInfo(allAvatarInfo);
        SceneManager.LoadScene("MainGame");
    }

    public override void notify_match_info(byte curNum)
    {
        Dbg.INFO_MSG("PlayerAvatar::onMatch" + curNum);

        if (firstMatch)
            SceneManager.LoadScene("Match");
        else
            firstMatch = false;

        KBEngine.Event.fireOut("OnMatchNumChange", new object[] { curNum });
    }
}