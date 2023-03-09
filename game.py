import time, json

# from https://stackoverflow.com/a/44543367/4542015
#
def send_key_event(driver, name, options={}):
    options["type"] = name
    body = json.dumps({"cmd": "Input.dispatchKeyEvent", "params": options})
    resource = "/session/%s/chromium/send_command" % driver.session_id
    url = driver.command_executor._url + resource
    driver.command_executor._request("POST", url, body)

#change 
def press_key(driver, key):
    FPS = driver.execute_script("return FPS")
    duration = FPS / 200
    endtime = time.time() + duration
    options = {"windowsVirtualKeyCode": key}

    while True:
        send_key_event(driver, "rawKeyDown", options)
        send_key_event(driver, "char", options)

        if time.time() > endtime:
            send_key_event(driver, "keyUp", options)
            break

        options["autoRepeat"] = True
        time.sleep(0.01)


class GameData:
    def __init__(self, driver):
        self.driver = driver
        self.level = 1
        self.enemies_amount = self.get_enemies_amount()
        self.coins_amount = self.get_coins_amount()
        self.collected_coins = self.get_collected_coins()
        self.end_distance = self.get_end_distance()

    def get_FPS(self):
        return self.driver.execute_script("return getFPS()")

    def set_FPS(self, FPS):
        s = "setFPS(" + str(FPS) + ")"
        return self.driver.execute_script(s)

    def get_level(self):
        return self.driver.execute_script("return getLevel()")

    def get_data(self):
        s = "return getData(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def get_enemies_amount(self):
        s = "return getEnemiesAmount(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def get_coins_amount(self):
        s = "return getCoinsAmount(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def get_collected_coins(self):
        s = "return getCoinsCollected()"
        return self.driver.execute_script(s)

    def get_enemies_pos(self):
        s = "return getEnemiesPos(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def get_coins_pos(self):
        s = "return getCoinsPos(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def get_player_pos(self):
        return self.driver.execute_script("return getPlayerPos()")

    def get_end_distance(self):
        s = "return getEndDistance(" + str(self.level) + ")"
        return self.driver.execute_script(s)

    def update_enemies_amount(self):
        self.enemies_amount = self.get_enemies_amount()

    def update_coins_amount(self):
        self.coins_amount = self.get_coins_amount()

    def update_end_distance(self):
        self.end_distance = self.get_end_distance()

    def update_level(self):
        self.level = self.get_level()

    def update_data(self):
        self.update_coins_amount()
        self.update_end_distance()
        self.update_enemies_amount()
        self.update_level()


class ActionKeys:
    up = ord("W")
    down = ord("S")
    left = ord("A")
    right = ord("D")
    none = ord("Q")  # this key does nothing in game


class GameInput:
    def __init__(self, driver):
        self.driver = driver

    def up(self):
        press_key(self.driver, ActionKeys.up)

    def down(self):
        press_key(self.driver, ActionKeys.down)

    def left(self):
        press_key(self.driver, ActionKeys.left)

    def right(self):
        press_key(self.driver, ActionKeys.right)

    def none(self):
        press_key(self.driver, ActionKeys.none)
