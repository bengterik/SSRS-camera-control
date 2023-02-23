class KeyBoard:
    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.pitch = self.add_sat(self.pitch, DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
    
            elif key == keyboard.Key.down:
                self.pitch = self.add_sat(self.pitch, -DEGREE_PER_KEY_PRESS, PITCH_MIN, PITCH_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)
            
            elif key == keyboard.Key.left:
                self.yaw = self.add_sat(self.yaw, -DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif key == keyboard.Key.right:
                self.yaw = self.add_sat(self.yaw, DEGREE_PER_KEY_PRESS, YAW_MIN, YAW_MAX)
                self.connection.gimbal_pitch_yaw(self.pitch, self.yaw)

            elif key.char == 'r':
                self.connection.gimbal_retract()
                self.pitch = PITCH_RETRACTED
                self.yaw = YAW_RETRACTED
                
            elif key.char == 'n':
                self.connection.gimbal_neutral()
                self.pitch = PITCH_NEUTRAL
                self.yaw = YAW_NEUTRAL

            elif key == keyboard.Key.esc:
                # Stop listener
                return False
            
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
        
        print("pitch: %s, yaw: %s" % (self.pitch, self.yaw))

    def activate_gimbal_control_keys(self):
        
        listener = keyboard.Listener(
            on_press=self.on_press)
        
        listener.start()
        
        print("Keyboard control activated. Press ESC to exit.")