import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QPen, QPalette, QBrush, QImage, QPixmap
from time import sleep 
from PyQt5.QtCore import Qt, pyqtSlot
import PyQt5.QtMultimedia as M
from threading import Thread
from Score import Score

 
class Dot_man(QWidget):
  def __init__(self):
    super().__init__()
    self._music = M.QSound('intro.wav')
    self._music.setLoops(-1)
    self._music.play()
    self._score = '                                   '
    self._lives = '   '
    self._bm_x_pos = 2
    self._t = Thread(target=self._winGame)
    self._screen_bottom = 600
    self._bm_height = 10
    self._bm_y_pos = self._screen_bottom - self._bm_height
    self._jump_start = self._screen_bottom - self._bm_height
    self._screen_l_edge = 0
    self._screen_r_edge = 550
    self._param_list = [(200,580,300,580),(320,570,420,570),(190,550,290,550),(180,520,280,520),(120,500,160,500),(120,470,160,470),
                       (130,440,165,440),(140,410,150,410),(170,390,300,390),(340,400,390,400),(350,370,380,370),(355,350,375,350),
                       (355,320,375,320),(255,320,315,320),(180,290,240,290),(100,350,120,350),(20,320,80,320),(20,290,80,290),
                       (20,260,80,260),(20,230,80,230),(95,200,105,200),(135,210,155,210),(185,200,205,200),(225,190,265,190),
                       (335,260,400,260),(415,230,425,230),(390,200,400,200),(415,170,425,170),(390,140,400,140),(355,110,375,110),
                       (250,150,300,150)]
    self._goal_param = [350,50,30,30]
    self._dot_color = Qt.black
    self._goal_color_list = [Qt.blue,Qt.red,Qt.yellow,Qt.green]
    self._goal_color = Qt.cyan
    self._alive = True
    self._game_on = False
    self._flash_on = False
    self._draw_portal = False
    self._in_air = False
    self._initUI()

  def _initUI(self):
    self._button = QPushButton('Start', self)
    self._button.move(225,200)
    self._button.clicked.connect(self._startGame)
    self._labl_1 = QLabel('           ', self)
    self._labl_1.move(0,0)
    self._labl_1a = QLabel(self._score, self)
    self._labl_1a.move(45,0)
    self._labl_2 = QLabel('                        ', self)
    self._labl_2.move(245,0)
    self._labl_3 = QLabel('           ', self)
    self._labl_3.move(450,0)
    self._labl_3a = QLabel(self._lives, self)
    self._labl_3a.move(495,0)
    self._labl_4 = QLabel('''
                                              ''', self)
    self._labl_4.move(210,300)
    self.setGeometry(300,300,self._screen_r_edge,600)
    self.setWindowTitle('Dot Man')
    i = QImage("images.jpg")
    p = QPalette()
    p.setBrush(10,QBrush(QPixmap(i).scaled(550,600,transformMode=Qt.SmoothTransformation)))
    self.setPalette(p)
    self.show()
  
  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    self._makeSprite(qp)
    self._makePlatform(qp,self._param_list)
    self._goal(qp)
    qp.end()
  
  def _update_app(self,sleep_time = 0):
    self.update()
    QApplication.processEvents()
    sleep(sleep_time)
  
  def _check_if_life_lost(self,too_high):
    if self._bm_y_pos - too_high >= 150: # make death function
      george.lose_life()
      self._lives = str(george.get_lives())
      self._labl_3a.setText(self._lives)
      if self._lives == '0':
        self._lives = str(george.get_lives())
        self._labl_3a.setText(self._lives)
        self._gameOver()
        return True
      self._startGame()
      return True
    return False
        
  def _land(self):
    self._jump_start = self._bm_y_pos
    self._dot_color = Qt.black
    self._in_air = False
    
  def _increment_position(self,x,y):
    self._bm_y_pos += y
    self._bm_x_pos += x
    self._isOnScreen()
  
  def _music_player(self,sng,loops=-1 ): 
      self._music.stop()
      self._music = M.QSound(sng)
      self._music.setLoops(loops)
      self._music.play()
  @pyqtSlot()  
  def _startGame(self):
    self._bm_x_pos = 2      #
    self._bm_y_pos = self._screen_bottom - self._bm_height    #
    self._jump_start = self._screen_bottom - self._bm_height    #
    self._music_player('in_game.wav',-1)
    self._game_on = True
    self._button.resize(0,0)
    self._update_labels(None,str(george.get_score()),None,None,str(george.get_lives()),None)
    if not self._alive:
      while int(george.get_lives()) < 3:
        george.gain_life()
      self._lives = str(george.get_lives())
      self._alive = True
      self._update_labels(None,str(george.get_score()),'Level 1',
                           None,str(george.get_lives()),'')
    self.update()
  
  def _update_labels(self,labl1,labl1a,labl2,labl3,labl3a,labl4): 
    labl_list = [self._labl_1,self._labl_1a,self._labl_2,self._labl_3,
                 self._labl_3a,self._labl_4]
    labl_value_list = [labl1,labl1a,labl2,labl3,labl3a,labl4]
    for i in range(6):
      if labl_value_list[i] != None:
        labl_list[i].setText(labl_value_list[i])
  
  def _nextLevel(self):
    self._update_labels('','','','','',
    '''        You Win!!! 
    Level 2 coming soon''')
    self._music_player('game_over.wav',-1)
    self._button.setText('Play Again?')
    self._button.resize(self._button.sizeHint())
    self._bm_height = 10
    self._bm_x_pos = 2
    self._bm_y_pos = self._screen_bottom - self._bm_height
    self._alive = False
    self._draw_portal = False
  
  def _touch_goal(self):
    if self._game_on:
      if self._bm_y_pos == (self._goal_param[1] + self._goal_param[2]) and self._bm_x_pos >= self._goal_param[0] and  (self._bm_x_pos <= self._goal_param[0] + self._goal_param[2]):  
        self._flash_on = True
        self._draw_portal = True
        george.add_points(1000)
        return True
      return False
        
  def _winGame(self):
      if self._game_on:
        while self._flash_on:
          for i in range(len(self._goal_color_list)):
            self._goal_color = self._goal_color_list[i] 
            self._update_app(.4)              
    
  def _gameOver(self):
    if self._lives == '0':
      self._game_on = False
      self._music_player('game_over.wav',-1)
      george.subtract_points(int(george.get_score()))
      self._update_labels('','','Game Over','','',None)
      self._button.setText('Continue?')
      self._button.resize(self._button.sizeHint())
      self._bm_x_pos = 2
      self._bm_y_pos = self._screen_bottom - self._bm_height
      self._alive = False
      self._update_app()
              
  def _isOnPlatform(self):
    if self._game_on:
      for tup in self._param_list[0:-1]:
        if self._bm_y_pos == (tup[1] - self._bm_height) and self._bm_x_pos >= tup[0] - self._bm_height and  self._bm_x_pos <= tup[2]:
          return True
      return False
  
  def _isOnScreen(self): #Get a better name
    if self._game_on:
      if self._bm_x_pos < self._screen_l_edge:
        self._bm_x_pos = self._screen_l_edge
      if self._bm_x_pos > (self._screen_r_edge -self._bm_height):
        self._bm_x_pos = self._screen_r_edge -self._bm_height
            
      
  def _jump(self,x,y):
    if self._game_on:
      self._in_air = True
      max_jump_height =(self._jump_start - 40)
      while self._bm_y_pos > max_jump_height: #makes _jump height 50 pixels
        if self._touch_goal():
          if self._t.ident == None: # Change this if block
            self._t.start()
          break
        self._increment_position(x,y)
        if self._bm_y_pos == max_jump_height: #Maybee take this out of final
          self._dot_color = Qt.blue                    
        self._update_app(.01)
  
  def _fall(self,x,y):
    too_high = self._bm_y_pos
    if self._game_on:
      self._in_air = True
      on_ground = (self._screen_bottom - self._bm_height)
      while self._bm_y_pos < on_ground and self._in_air:
        if self._isOnPlatform():
          if self._check_if_life_lost(too_high):
            pass
          else:
            george.add_points(100)
            self._score = str(george.get_score())
            self._labl_1a.setText(self._score)
          self._land()
          self._update_app()
          break
        else:
          self._increment_position(x,y)
          if self._bm_y_pos >= on_ground:
            self._check_if_life_lost(too_high)
            self._dot_color = Qt.black
            self.update()
            break
          self._update_app(.01)
      self._land()
      return None
  
  def __pen_setup(self,color,width,qp):    
    r = QPen(color, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    qp.setPen(r)
    return r
  def _makePlatform(self, qp,lst): #_param_list is a list of parameters for drawLine()
    if self._game_on:
      self._labl_1.setText('Score:')
      self._labl_2.setText('Level 1')
      self._labl_3.setText('Lives:')
      for tup in lst[0:-1]:
        r = self.__pen_setup(Qt.black,5,qp)
        qp.drawLine(*tup)
      if self._draw_portal:
        r.setBrush(Qt.yellow)
        qp.setPen(r)
        qp.drawLine(*lst[-1])
        
  def _makeSprite(self, qp):
    if self._game_on:
      if self._bm_y_pos == (self._param_list[-1][1] - self._bm_height) and self._bm_x_pos >= self._param_list[-1][0] - self._bm_height and  self._bm_x_pos <= self._param_list[-1][2]:
        if self._draw_portal:
          self._flash_on = False
          self.__pen_setup(self._dot_color,1,qp)
          self._bm_height = 0
          qp.drawRect(self._bm_x_pos,self._bm_y_pos,self._bm_height,self._bm_height)
          self._game_on = False
          self._nextLevel()
          self._t.join()
      else:
        self.__pen_setup(self._dot_color,1,qp)
        #r.setColor(self._dot_color)
        #qp.setPen(r)
        qp.setBrush(self._dot_color)   
        qp.drawRect(self._bm_x_pos,self._bm_y_pos,self._bm_height,self._bm_height)

  def _goal(self,qp):
    if self._game_on:
      self.__pen_setup(self._goal_color,5,qp)
      qp.setBrush(self._goal_color)
      qp.drawRect(*self._goal_param)
  
  def keyPressEvent(self, e):
    if self._game_on:
      if e.key() == Qt.Key_Right:
        if not self._in_air:
          self._bm_x_pos += 5
          self._isOnScreen()
          if not self._isOnPlatform():
            self._fall(0,2)
          self.update()
      if e.key() == Qt.Key_Left:
        if not self._in_air:
          self._bm_x_pos -= 5
          self._isOnScreen()
          if not self._isOnPlatform():
            self._fall(0,2)
          self.update()
      if e.key() == Qt.Key_A:
        if self._in_air == False:
          self._jump(-1,-2)
          self._fall(-1,2)
      if e.key() == Qt.Key_L:
        if self._in_air == False:
          self._jump(1,-2)
          self._fall(1,2)
      if e.key() == Qt.Key_Up:
        if self._in_air == False:
          self._jump(0,-2)
          self._fall(0,2)
          
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dottie = Dot_man()
    george = Score('George')
    sys.exit(app.exec_())