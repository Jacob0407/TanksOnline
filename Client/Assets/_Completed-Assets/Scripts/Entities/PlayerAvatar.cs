using UnityEngine;
using UnityEditor;
using KBEngine;

public class PlayerAvatar : PlayerAvatarBase
{
    public override void onEnter()
    {
        Dbg.INFO_MSG("PlayerAvatar::onEnter");
    }
}