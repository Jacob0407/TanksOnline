using UnityEngine;
using UnityEditor;
using KBEngine;
using UnityEngine.SceneManagement;
using Complete;

public class PlayerAvatar : PlayerAvatarBase
{
    private bool firstMatch = true;

    public override void onEnter()
    {
        GameManager.g_Player = this;
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
}