using UnityEngine;
using UnityEditor;
using KBEngine;
using UnityEngine.SceneManagement;

public class PlayerAvatar : PlayerAvatarBase
{
    public override void onEnter()
    {
        Dbg.INFO_MSG("PlayerAvatar::onEnter");
        this.baseEntityCall.reqMatch();
    }

    public override void onEnterBattleRoom()
    {
        SceneManager.LoadScene("MainGame");
    }

    public override void onMatch(uint arg1)
    {
        Dbg.INFO_MSG("PlayerAvatar::onMatch" + arg1);
    }
}