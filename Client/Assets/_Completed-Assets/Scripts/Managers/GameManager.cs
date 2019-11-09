using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using KBEngine;
using System.Collections.Generic;

namespace Complete
{
    public class GameManager : MonoBehaviour
    {
        public int m_NumRoundsToWin = 5;            // The number of rounds a single player has to win to win the game.
        public float m_StartDelay = 3f;             // The delay between the start of RoundStarting and RoundPlaying phases.
        public float m_EndDelay = 3f;               // The delay between the end of RoundPlaying and RoundEnding phases.
        public CameraControl m_CameraControl;       // Reference to the CameraControl script for control during different phases.
        public Text m_MessageText;                  // Reference to the overlay Text to display winning text, etc.
        public GameObject m_TankPrefab;             // Reference to the prefab the players will control.

        public static PlayerAvatar g_MainPlayer;           // 主玩家
        public static Dictionary<ENTITY_ID, PlayerAvatar> g_OtherPlayers = new Dictionary<ENTITY_ID, PlayerAvatar>();  // 其他非主玩家

        
        private int m_RoundNumber;                  // Which round the game is currently on.
        private WaitForSeconds m_StartWait;         // Used to have a delay whilst the round starts.
        private WaitForSeconds m_EndWait;           // Used to have a delay whilst the round or game ends.
        private TankManager m_RoundWinner;          // Reference to the winner of the current round.  Used to make an announcement of who won.
        private TankManager m_GameWinner;           // Reference to the winner of the game.  Used to make an announcement of who won.
        private static AVATAR_INFO_LIST m_allAvatarBaseInfo;        // 所有玩家的基本数据

        private void Start()
        {
            // Create the delays so they only have to be made once.
            m_StartWait = new WaitForSeconds (m_StartDelay);
            m_EndWait = new WaitForSeconds (m_EndDelay);
            EnterBattleGame();
        }

        public static void SetAllAvatarBaseInfo(AVATAR_INFO_LIST data)
        {
            m_allAvatarBaseInfo = data;
        }

        public void EnterBattleGame()
        {
            SpawnAllTanks();
            SetCameraTargets();

            // Once the tanks have been created and the camera is using them as targets, start the game.
            StartCoroutine(GameLoop());
        }


        private void SpawnAllTanks()
        {
            foreach (var avatar in m_allAvatarBaseInfo.values)
            {
                if (g_MainPlayer.id == avatar.entity_id)
                {
                    if (g_MainPlayer == null)
                        continue;

                    // 主客户端
                    g_MainPlayer.m_TankManager.m_Instance = Instantiate(m_TankPrefab, avatar.born_position, new Quaternion(0, avatar.born_yaw, 0, 0)) as GameObject;
                    g_MainPlayer.m_TankManager.m_PlayerNumber = 1;
                    g_MainPlayer.m_TankManager.Setup();
                }
                else
                {
                    if (!g_OtherPlayers.ContainsKey(avatar.entity_id))
                        continue;

                    TankManager tank = new TankManager
                    {
                        m_Instance = Instantiate(m_TankPrefab, avatar.born_position, new Quaternion(0, avatar.born_yaw, 0, 0)) as GameObject,
                        m_PlayerNumber = avatar.entity_id
                    };
                    tank.Setup();
                    g_OtherPlayers[avatar.entity_id].m_TankManager = tank;
                }
            }
        }


        private void SetCameraTargets()
        {
            // Create a collection of transforms the same size as the number of tanks.
            Transform[] targets = new Transform[m_allAvatarBaseInfo.values.Count];

            targets[0] = g_MainPlayer.m_TankManager.m_Instance.transform;
            int index = 1;
            foreach (var tank in g_OtherPlayers)
            {
                targets[index] = tank.Value.m_TankManager.m_Instance.transform;
            }
            
            // These are the targets the camera should follow.
            m_CameraControl.m_Targets = targets;
        }


        // This is called from start and will run each phase of the game one after another.
        private IEnumerator GameLoop ()
        {
            // Start off by running the 'RoundStarting' coroutine but don't return until it's finished.
            yield return StartCoroutine (RoundStarting ());

            // Once the 'RoundStarting' coroutine is finished, run the 'RoundPlaying' coroutine but don't return until it's finished.
            yield return StartCoroutine (RoundPlaying());

            // Once execution has returned here, run the 'RoundEnding' coroutine, again don't return until it's finished.
            yield return StartCoroutine (RoundEnding());

            // This code is not run until 'RoundEnding' has finished.  At which point, check if a game winner has been found.
            if (m_GameWinner != null)
            {
                // If there is a game winner, restart the level.
                SceneManager.LoadScene (0);
            }
            else
            {
                // If there isn't a winner yet, restart this coroutine so the loop continues.
                // Note that this coroutine doesn't yield.  This means that the current version of the GameLoop will end.
                StartCoroutine (GameLoop ());
            }
        }


        private IEnumerator RoundStarting ()
        {
            // As soon as the round starts reset the tanks and make sure they can't move.
            ResetAllTanks ();
            DisableTankControl ();

            // Snap the camera's zoom and position to something appropriate for the reset tanks.
            m_CameraControl.SetStartPositionAndSize ();

            // Increment the round number and display text showing the players what round it is.
            m_RoundNumber++;
            m_MessageText.text = "ROUND " + m_RoundNumber;

            // Wait for the specified length of time until yielding control back to the game loop.
            yield return m_StartWait;
        }


        private IEnumerator RoundPlaying ()
        {
            // As soon as the round begins playing let the players control the tanks.
            EnableTankControl ();

            // Clear the text from the screen.
            m_MessageText.text = string.Empty;

            // While there is not one tank left...
            while (!OneTankLeft())
            {
                // ... return on the next frame.
                yield return null;
            }
        }


        private IEnumerator RoundEnding ()
        {
            // Stop tanks from moving.
            DisableTankControl ();

            // Clear the winner from the previous round.
            m_RoundWinner = null;

            // See if there is a winner now the round is over.
            m_RoundWinner = GetRoundWinner ();

            // If there is a winner, increment their score.
            if (m_RoundWinner != null)
                m_RoundWinner.m_Wins++;

            // Now the winner's score has been incremented, see if someone has one the game.
            m_GameWinner = GetGameWinner ();

            // Get a message based on the scores and whether or not there is a game winner and display it.
            string message = EndMessage ();
            m_MessageText.text = message;

            // Wait for the specified length of time until yielding control back to the game loop.
            yield return m_EndWait;
        }


        // This is used to check if there is one or fewer tanks remaining and thus the round should end.
        private bool OneTankLeft()
        {
            return false;
        }
        
        
        // This function is to find out if there is a winner of the round.
        // This function is called with the assumption that 1 or fewer tanks are currently active.
        private TankManager GetRoundWinner()
        {
            // Go through all the tanks...
            foreach (var tankData in g_OtherPlayers)
            {
                if (tankData.Value.m_TankManager.m_Instance.activeSelf)
                    return tankData.Value.m_TankManager;
            }

            // If none of the tanks are active it is a draw so return null.
            return null;
        }


        // This function is to find out if there is a winner of the game.
        private TankManager GetGameWinner()
        {
            // Go through all the tanks...
            foreach (var tankData in g_OtherPlayers)
            {
                if (tankData.Value.m_TankManager.m_Wins == m_NumRoundsToWin)
                    return tankData.Value.m_TankManager;
            }

            // If no tanks have enough rounds to win, return null.
            return null;
        }


        // Returns a string message to display at the end of each round.
        private string EndMessage()
        {
            // By default when a round ends there are no winners so the default end message is a draw.
            string message = "DRAW!";

            // If there is a winner then change the message to reflect that.
            if (m_RoundWinner != null)
                message = m_RoundWinner.m_ColoredPlayerText + " WINS THE ROUND!";

            // Add some line breaks after the initial message.
            message += "\n\n\n\n";

            // Go through all the tanks and add each of their scores to the message.
            foreach (var tankData in g_OtherPlayers)
            {
                message += tankData.Value.m_TankManager.m_ColoredPlayerText + ": " + tankData.Value.m_TankManager.m_Wins + " WINS\n";
            }

            // If there is a game winner, change the entire message to reflect that.
            if (m_GameWinner != null)
                message = m_GameWinner.m_ColoredPlayerText + " WINS THE GAME!";

            return message;
        }


        // This function is used to turn all the tanks back on and reset their positions and properties.
        private void ResetAllTanks()
        {
            foreach (var tankData in g_OtherPlayers)
            {
                tankData.Value.m_TankManager.Reset();
            }
            
            g_MainPlayer.m_TankManager.Reset();
        }


        private void EnableTankControl()
        {
            g_MainPlayer.m_TankManager.EnableControl();
            foreach (var tankData in g_OtherPlayers)
            {
                tankData.Value.m_TankManager.EnableControl();
            }
        }


        private void DisableTankControl()
        {
            g_MainPlayer.m_TankManager.DisableControl();
            foreach (var tankData in g_OtherPlayers)
            {
                tankData.Value.m_TankManager.DisableControl();
            }
        }
    }
}