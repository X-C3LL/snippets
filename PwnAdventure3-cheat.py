# Small cheat for Pwn Adventure 3 used as tutorial for Frida
# Author: Juan Manuel Fernández (@TheXC3LL)


import frida
import sys

session = frida.attach("PwnAdventure3-Linux-Shipping")
script = session.create_script("""
        // Global Values
        var Player = {
            m_walkingSpeed : 200,
        };

        // Cheat status
        var cheatStatus = {
            walkingSpeed : 0,
            infiniteMana : 0
        };

        //Teleport
        var setPositionAddr = Module.findExportByName("libGameLogic.so", "_ZN5Actor11SetPositionERK7Vector3");
        var setPosition = new NativeFunction(setPositionAddr, 'void', ['pointer', 'pointer']);
        var Vector3 = Memory.alloc(16);

        function teleport(thisReference, x, y, z) {
            Memory.writeFloat(Vector3, x);
            Memory.writeFloat(ptr(Vector3).add(4), y);
            Memory.writeFloat(ptr(Vector3).add(8), z);
            setPosition(thisReference, Vector3);
        }


        // Chat Helper
        function chatHelper(msg, thisReference) {
            var token = msg.split(" ");
            if (token[0] === "!wspeed_on") {
                Player.m_walkingSpeed = parseInt(token[1]);
                cheatStatus.walkingSpeed = 1;
                console.log("[CHEAT]: Walking Speed Enabled (" + token[1] + ")");
            }
            if (token[0] === "!wspeed_off") {
                Player.m_walkingSpeed = 200;
                cheatStatus.walkingSpeed = 0;
                console.log("[CHEAT]: Walking Speed Disabled (200)");
            }
            if (token[0] === "!tp") {
                console.log("[CHEAT]: Teleporting to " + token[1] + " " + token[2] + " "+ token[3]);
                teleport(thisReference, parseInt(token[1]), parseInt(token[2]), parseInt(token[3]));
            }
            if (token[0] === "!mana_on") {
                cheatStatus.infiniteMana = 1;
                console.log("[CHEAT]: Infinite Mana Enabled");
            }
            if (token[0] === "!mana_off") {
                cheatStatus.infiniteMana = 0;
                console.log("[CHEAT]: Infinite Mana Disabled");
            }
        }


        //Find "Player::Chat"
        var chat = Module.findExportByName("libGameLogic.so", "_ZN6Player4ChatEPKc");
        console.log("Player::Chat() at  address: " + chat);

        // Add our logger
        Interceptor.attach(chat, {
            onEnter: function (args) { // 0 => this; 1 => cont char* (our text)
               var chatMsg = Memory.readCString(args[1]);
               console.log("[Chat]: " + chatMsg);
               chatHelper(chatMsg, args[0]);
            }

        });

        // Find Player::GetWalkingSpeed()
        var walkSpeed = Module.findExportByName("libGameLogic.so", "_ZN6Player15GetWalkingSpeedEv");
        console.log("Player::GetWalkingSpeed() at address: " + walkSpeed);

        // Check Speed
        Interceptor.attach(walkSpeed,
            {
                // Get Player * this location
                onEnter: function (args) {
                    //console.log("Player at address: " + args[0]);
                    this.walkingSpeedAddr = ptr(args[0]).add(736) // Offset m_walkingSpeed
                    //console.log("WalkingSpeed at address: " + this.walkingSpeedAddr);
                },

                // Get the return value
                onLeave: function (retval) {
                    if (Memory.readFloat(this.walkingSpeedAddr) != Player.m_walkingSpeed && cheatStatus.walkingSpeed == 0) {
                        Memory.writeFloat(this.walkingSpeedAddr, 200);
                    }
                    if (cheatStatus.walkingSpeed == 1) {
                        Memory.writeFloat(this.walkingSpeedAddr, Player.m_walkingSpeed);
                    }
                }
            });

        // Mana cheat - (Update 08/JUL/2018: It's fake. Only updates the mana value in the HUD)
        var getMana = Module.findExportByName("libGameLogic.so", "_ZN6Player7GetManaEv");
        console.log("Player::GetMana at address: " + getMana);
        Interceptor.attach(getMana,
        {
            onEnter: function (args) {
                if (cheatStatus.infiniteMana == 1) {
                    m_manaAddr = ptr(args[0]).add(544) // Offset m_mana
                    Memory.writeInt(m_manaAddr, 100);
                }
            }
        }

        );






""")

script.load()
sys.stdin.read()



