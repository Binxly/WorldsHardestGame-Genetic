setFPS = newFPS => {
  FPS = newFPS;
  setInterval(function() {
    update();
    draw();
  }, 1000 / FPS);
};

getFPS = () => FPS;

getLevel = () => level;

getPlayerPos = () => [player.x, player.y];

getEnemiesPos = level => {
  a = enemies[level].map(a => [a.x, a.y]).flat();
  len = a.length;
  a.length = 322;
  a.fill(0, len, 322);
  return a;
};

getEnemiesAmount = level => {
  return enemies[level].length;
};

getCoinsPos = level => {
  a = coins[level].map(a => [a.x, a.y]).flat();
  len = a.length;
  a.length = 270;
  a.fill(0, len, 270);
  return a;
};

getCoinsAmount = level => {
  return coins[level].length;
};

getData = level => {
  return [...getPlayerPos(), ...getEnemiesPos(level), ...getCoinsPos(level)];
};

getEndDistance = level => {
  a = player.x - checkpoints[level][checkpoints[level].length - 1][0] * 40 - 16;
  b = player.y - checkpoints[level][checkpoints[level].length - 1][1] * 40 - 30;
  return Math.hypot(a, b);
};
