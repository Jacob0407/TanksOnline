using UnityEngine;
using KBEngine;

namespace Complete
{
    public class TankMovement : MonoBehaviour
    {
        public int m_PlayerNumber = 1;              // Used to identify which tank belongs to which player.  This is set by this tank's manager.
        public float m_Speed = 12f;                 // How fast the tank moves forward and back.
        public float m_TurnSpeed = 180f;            // How fast the tank turns in degrees per second.
        public AudioSource m_MovementAudio;         // Reference to the audio source used to play engine sounds. NB: different to the shooting audio source.
        public AudioClip m_EngineIdling;            // Audio to play when the tank isn't moving.
        public AudioClip m_EngineDriving;           // Audio to play when the tank is moving.
		public float m_PitchRange = 0.2f;           // The amount by which the pitch of the engine noises can vary.

        private string m_MovementAxisName;          // The name of the input axis for moving forward and back.
        private string m_TurnAxisName;              // The name of the input axis for turning.
        private Rigidbody m_Rigidbody;              // Reference used to move the tank.
        private float m_MovementInputValue;         // The current value of the movement input.
        private float m_TurnInputValue;             // The current value of the turn input.
        private float m_OriginalPitch;              // The pitch of the audio source at the start of the scene.
        private ParticleSystem[] m_particleSystems; // References to all the particles systems used by the Tanks

        private void Awake ()
        {
            m_Rigidbody = GetComponent<Rigidbody> ();
        }


        private void OnEnable ()
        {
            // When the tank is turned on, make sure it's not kinematic.
            m_Rigidbody.isKinematic = false;

            // Also reset the input values.
            m_MovementInputValue = 0f;
            m_TurnInputValue = 0f;

            // We grab all the Particle systems child of that Tank to be able to Stop/Play them on Deactivate/Activate
            // It is needed because we move the Tank when spawning it, and if the Particle System is playing while we do that
            // it "think" it move from (0,0,0) to the spawn point, creating a huge trail of smoke
            m_particleSystems = GetComponentsInChildren<ParticleSystem>();
            for (int i = 0; i < m_particleSystems.Length; ++i)
            {
                m_particleSystems[i].Play();
            }
        }


        private void OnDisable ()
        {
            // When the tank is turned off, set it to kinematic so it stops moving.
            m_Rigidbody.isKinematic = true;

            // Stop all particle system so it "reset" it's position to the actual one instead of thinking we moved when spawning
            for(int i = 0; i < m_particleSystems.Length; ++i)
            {
                m_particleSystems[i].Stop();
            }
        }


        private void Start ()
        {
            if (m_PlayerNumber != 1)
                return;

            // The axes names are based on player number.
            m_MovementAxisName = "Vertical" + m_PlayerNumber;
            m_TurnAxisName = "Horizontal" + m_PlayerNumber;

            // Store the original pitch of the audio source.
            m_OriginalPitch = m_MovementAudio.pitch;
        }


        private void Update ()
        {
            if (m_PlayerNumber != 1)
                return;

            // Store the value of both input axes.
            m_MovementInputValue = Input.GetAxis (m_MovementAxisName);
            m_TurnInputValue = Input.GetAxis (m_TurnAxisName);

            EngineAudio ();
        }


        private void EngineAudio ()
        {
            // If there is no input (the tank is stationary)...
            if (Mathf.Abs (m_MovementInputValue) < 0.1f && Mathf.Abs (m_TurnInputValue) < 0.1f)
            {
                // ... and if the audio source is currently playing the driving clip...
                if (m_MovementAudio.clip == m_EngineDriving)
                {
                    // ... change the clip to idling and play it.
                    m_MovementAudio.clip = m_EngineIdling;
                    m_MovementAudio.pitch = Random.Range (m_OriginalPitch - m_PitchRange, m_OriginalPitch + m_PitchRange);
                    m_MovementAudio.Play ();
                }
            }
            else
            {
                // Otherwise if the tank is moving and if the idling clip is currently playing...
                if (m_MovementAudio.clip == m_EngineIdling)
                {
                    // ... change the clip to driving and play.
                    m_MovementAudio.clip = m_EngineDriving;
                    m_MovementAudio.pitch = Random.Range(m_OriginalPitch - m_PitchRange, m_OriginalPitch + m_PitchRange);
                    m_MovementAudio.Play();
                }
            }
        }


        private void FixedUpdate ()
        {
            // Adjust the rigidbodies position and orientation in FixedUpdate.
            Move ();
            Turn ();
        }

        // 影子追随
        private float CalcNewValueByShadow(float curValue, float shadowValue, float deltaTime)
        {
            if (curValue == shadowValue)
                return curValue;

            float deltaValue = Mathf.Abs(curValue - shadowValue);
            int ratio = 1;
            if (curValue < shadowValue)
            {
                // 大于一定阈值，加速
                if (deltaValue > m_Speed * 40 * deltaTime)
                    ratio = 2;
                
                curValue += Mathf.Min(deltaValue, m_Speed * deltaTime * ratio);
            }
            else
            {
                if (deltaValue > m_Speed * 5 * deltaTime)
                    ratio = 2;

                curValue -= Mathf.Min(deltaValue, m_Speed * deltaTime * ratio);
            }

            return curValue;
        }

        private void Move ()
        {
            if (m_PlayerNumber != 1)
            {   
                PlayerAvatar avatar = GameManager.g_OtherPlayers[m_PlayerNumber];
                float newX = CalcNewValueByShadow(m_Rigidbody.position.x, avatar.position.x, Time.deltaTime);
                float newZ = CalcNewValueByShadow(m_Rigidbody.position.z, avatar.position.z, Time.deltaTime);
                
                m_Rigidbody.MovePosition(new Vector3(newX, avatar.position.y, newZ));
            }
            else
            {
                Vector3 movement = transform.forward * m_MovementInputValue * m_Speed * Time.deltaTime;

                m_Rigidbody.MovePosition(m_Rigidbody.position + movement);
                GameManager.g_MainPlayer.position = m_Rigidbody.position;
            }
        }


        private void Turn ()
        {
            if (m_PlayerNumber != 1)
            {
                PlayerAvatar avatar = GameManager.g_OtherPlayers[m_PlayerNumber];
                m_Rigidbody.MoveRotation(Quaternion.Euler(avatar.direction));
            }
            else
            {
                float turn = m_TurnInputValue * m_TurnSpeed * Time.deltaTime;

                Quaternion turnRotation = Quaternion.Euler(0f, turn, 0f);

                m_Rigidbody.MoveRotation(m_Rigidbody.rotation * turnRotation);
                GameManager.g_MainPlayer.direction = m_Rigidbody.rotation.eulerAngles;
            }
        }
    }
}