from dialogue import *
from avatar import *
from event import EventManager
import global_variables
class AvalogueController():
    def __init__(self, frame, d_model: DialogueModel, d_view: DialogueView, a_model: AvatarModel, a_view: AvatarView):
        self.frame = frame 

        self.a_model = a_model
        self.a_view = a_view
        self.d_view = d_view
        self.d_model = d_model

        self.curr_dialogue = None
        self.curr_avatar = None

        self.curr_avalogue = None #in form of a tuple?

        self.idle_avatar = self.a_model.find_obj('i_default')
        self.sad_idle_avatar = self.a_model.find_obj('i_sad')
        
        self.button_press = False
        
        self.btn_press_name = None
        self.func_btn = None
        #a tuple = first var is avatar, second var is dialogue
        self.avalogue_stack = deque()

        
        EventManager.subscribe("collision", self.on_collision)
        EventManager.subscribe("congratulations", self.on_congrats)
        EventManager.subscribe("mistake", self.on_mistake)
        self.update_btnpress()
        self.update_loop()


    def update_btnpress(self):

       if self.d_view.button_press:
            
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name
            self.func_btn = utils.find_func(self.btn_press_name)
            self.d_view.button_press = False
        
       if self.d_view.button_press_1:
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name_1
            self.func_btn = utils.find_func(self.btn_press_name)
            self.d_view.button_press_1 = False

       if self.d_view.button_press_2:
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name_2
            self.func_btn = utils.find_func(self.btn_press_name)
            self.d_view.button_press_2 = False
        

       Tk.after(self.frame, 50, self.update_btnpress)

    #the avatar is dependent on the dialogue
    def update_loop(self):

        if self.curr_avalogue is None:
            if not self.avalogue_stack:
                print("1 --- stack is empty and no current avatar")
                self.empty_view()
            else:
                print("2 --- a new avalogue is added to stack")
                self.curr_avalogue = self.avalogue_stack.pop()
                self.curr_avalogue[1].start_letterbyletter()
        else:
            if self.avalogue_stack:
                 if not (self.avalogue_stack[0])[1].queue_flag:
                    self.curr_avalogue[1].pause_letterbyletter()
                    temp = self.curr_avalogue
                    self.curr_avalogue = self.avalogue_stack.pop()
                    self.curr_avalogue[1].start_letterbyletter()
                    self.avalogue_stack.append(temp)
                    if temp[1].button_num != 0:
                        print("4 --- if the previous avalogue had buttons, disable it")
                        self.d_view.disable_buttons(temp[1].button_num)
        

            if not self.curr_avalogue[1].showing and not self.curr_avalogue[1].stopped:
               print("5 --- it is waiting for start (in seconds)")
               self.empty_view()

            elif self.curr_avalogue[1].showing and not self.curr_avalogue[1].stopped:
                 print("6 --- it is talking")
                 self.update_view()
                 #if self.curr_avalogue[1].queue_flag and self.curr_avalogue[1].wipe_with_button:
                    # print("7 --- if the avalogue that was showing, got hidden and now is showing again had buttons, enable it(should we?)")
                    # self.d_view.enable_buttons(self.curr_avalogue[1].button_num)

            elif not self.curr_avalogue[1].showing and self.curr_avalogue[1].stopped and not self.curr_avalogue[1].finished:
                print("8 --- full text is shown and is either waiting for button or to wipe")
                if self.curr_avalogue[0].type == "Talking":
                        #print("11 --- for talking it needs to be idle(default/sad) while waiting for button, and wipe?")
                        if self.curr_avalogue[0].emotion == "sad":
                            new_avalogue = (self.sad_idle_avatar, self.curr_avalogue[1])
                            self.curr_avalogue = new_avalogue
                        else:
                            new_avalogue = (self.idle_avatar, self.curr_avalogue[1])
                            self.curr_avalogue = new_avalogue                        
            
                if self.curr_avalogue[1].wipe_with_button:
                    print("9 --- waiting for buttons, enable it and if talking it should be idle")
                    self.d_view.enable_buttons(self.curr_avalogue[1].button_num)
                    
                    if self.curr_avalogue[1].key == "choice_q":
                        #print("!!! --- START COUNTDOWN")
                        EventManager.post_event("start_cntdwn", -1)
    
                self.update_view()   
            
            if self.curr_avalogue[1].finished:
                print("10 --- it is finished and needs to be empty")
                self.curr_avalogue = None

            
            if self.button_press:
                print(self.curr_avalogue[1].button_num)
                self.d_view.hide_buttons(self.curr_avalogue[1].button_num)
                self.curr_avalogue = None
                self.button_press = False
                self.btn_press_name = None
                self.func_btn()

        Tk.after(self.frame, 100, self.update_loop)
       
       
    '''
               #if there is no new avalogue, d is empty and a is idle
        if not self.avalogue_stack and self.curr_avalogue is None:
            self.empty_view()
            
        #if a new avalogue shows up
        if self.avalogue_stack and self.curr_avalogue is None:
            self.curr_avalogue = self.avalogue_stack.pop()
            self.curr_avalogue[1].start_letterbyletter()

        #if in the midst of a new avalogue, a new one comes up that hasn't been used
        if self.avalogue_stack and self.curr_avalogue != None and not (self.avalogue_stack[0])[1].queue_flag:
            
            self.curr_avalogue[1].pause_letterbyletter()
            temp = self.curr_avalogue
            self.curr_avalogue = self.avalogue_stack.pop()
            self.curr_avalogue[1].start_letterbyletter()
            self.avalogue_stack.append(temp)
            
            if temp[1].button_num != 0:
                self.d_view.disable_buttons(temp[1].button_num)
            

        if self.curr_avalogue is not None and self.curr_avalogue[1].showing:        
            
            if self.curr_avalogue[1].queue_flag and not self.curr_avalogue[1].showing:
                print("sdfsdf")
                self.d_view.enable_buttons(self.curr_avalogue[1].button_num)
            
            self.update_view()
            
        if self.curr_avalogue is not None and not self.curr_avalogue[1].showing and not self.curr_avalogue[0].finished:
            self.update_view()             
            #full dialogue shown, avatar is idle, waiting for button press
            if self.curr_avalogue[1].button_num != 0:    
                self.d_view.enable_buttons(self.curr_avalogue[1].button_num)
                new_avalogue = (self.idle_avatar, self.curr_avalogue[1])
                self.curr_avalogue = new_avalogue
                self.update_view()
                if self.curr_avalogue[1].key == "choice_q":
                    EventManager.post_event("start_cntdwn", -1)
                

        #if the current dialogue is finished (for non-button mode, it's wiped actually), Avatar should be idle here
        if self.curr_avalogue is not None and self.curr_avalogue[1].finished:
            self.curr_avalogue = None
        
        if self.button_press:
            self.d_view.hide_buttons(self.curr_avalogue[1].button_num)
            func = utils.find_func(self.btn_press_name)
            self.curr_avalogue = None
            self.button_press = None
            self.btn_press_name = None
            func()

       ''' 

    


    


    def update_view(self):
        self.d_view.set_sentence(self.curr_avalogue[1].shown_text)
        img = self.curr_avalogue[0].get_currimage()
        self.a_view.set_image(img)

    def empty_view(self):
        self.d_view.set_sentence('')
        img = self.idle_avatar.get_currimage()
        self.a_view.set_image(img)

    def set_avalogue(self, a_key, d_key):
        
        avatar_obj  = self.a_model.find_obj(a_key)
        
        dialogue_obj = self.d_model.find_obj(d_key)
        
        self.d_view.init_buttons(dialogue_obj.button_num, 
                               dialogue_obj.button_title,
                                dialogue_obj.button1_title,
                                dialogue_obj.button2_title)
        
        self.avalogue_stack.append((avatar_obj, dialogue_obj))
   

    def on_congrats(self, dummy):
        self.set_avalogue("r_happy", "congrats")
    
    def on_mistake(self, dummy):
        if global_variables.jackalai_active:
            self.set_avalogue("r_sad", "mistake")
    
    def on_collision(self, dummy):
        
        self.set_avalogue("r_sad", "collision")

        
        

        