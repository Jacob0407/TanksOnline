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

    public override void onEnterBattleRoom(AVATAR_INFO_LIST allAvatarInfo)
    {
        GameManager.SetAllAvatarBaseInfo(allAvatarInfo);
        SceneManager.LoadScene("MainGame");
    }

    public override void onMatch(uint curNum)
    {
        Dbg.INFO_MSG("PlayerAvatar::onMatch" + curNum);
        if (firstMatch)
            SceneManager.LoadScene("Match");
        else
            firstMatch = false;
    }

    public override void onEnterWorld()
    {
        if (this.isPlayer())
            GameManager.g_MainPlayer = this;
        else
            GameManager.g_OtherPlayers[this.id] = this;
    }
}