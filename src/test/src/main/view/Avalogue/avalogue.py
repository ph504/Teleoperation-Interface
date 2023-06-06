from dialogue import *
from avatar import *

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
        
        self.button_press = False
        self.btn_press_name = None

        #a tuple = first var is avatar, second var is dialogue
        self.avalogue_stack = deque()

        
        self.update_btnpress()
        self.update_loop()


    def update_btnpress(self):

       if self.d_view.button_press:
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name
            self.d_view.button_press = False
        
       if self.d_view.button_press_1:
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name_1
            self.d_view.button_press_1 = False

       if self.d_view.button_press_2:
            self.button_press = True
            self.btn_press_name = self.d_view.button_press_name_2
            self.d_view.button_press_2 = False
        

       Tk.after(self.frame, 100, self.update_btnpress)


    #the avatar is dependent on the dialogue
    def update_loop(self):
        

        '''
         #if there is no dialogue
        if not self.dialogue_stack and self.curr_dialogue is None:
            self.view.set_sentence('')

        #if it's in complete idle mode (no new dialogues)
        if not self.avatar_stack and self.curr_avatar is None:
            img = self.idle_avatar.get_currimage()
            self.view.set_image(img)
        
        '''
        #if there is no new avalogue, d is empty and a is idle
        if not self.avalogue_stack and self.curr_avalogue is None:
            self.d_view.set_sentence('')
            img = self.idle_avatar.get_currimage()
            self.a_view.set_image(img)



        '''
        
        #if there is a new dialogue
        if self.dialogue_stack and self.curr_dialogue is None: 
            self.curr_dialogue = self.dialogue_stack.pop()
            self.curr_dialogue.start_letterbyletter()

        
        # If a new avatar shows up
        if self.avatar_stack and self.curr_avatar == None:
            
            self.curr_avatar = self.avatar_stack.pop()
        
        '''
        #if a new avalogue shows up
        if self.avalogue_stack and self.curr_avalogue is None:
            self.curr_avalogue = self.avalogue_stack.pop()
            self.curr_avalogue[1].start_letterbyletter()

        '''
            if self.avalogue_stack and self.curr_avalogue != None:
            av= self.avalogue_stack[0]
            print(av)
            d = av[1]
            print(d)
            print(d.queue_flag)
        '''

        
        
        '''
        #if in the middle of a dialogue, a "new" dialogue comes up that it's queue flag is not set (means it hasn't been used)
        #i did that because of what bug? because when the new bialogue came and then it finished, it again put it on the stack after the bigger one is finished.
        #since it's dialogue dependent ... makes sense to put that in avalogue
        if self.dialogue_stack and self.curr_dialogue != None and not self.dialogue_stack[0].queue_flag:
            self.curr_dialogue.pause_letterbyletter()
            temp = self.curr_dialogue
            self.curr_dialogue = self.dialogue_stack.pop()
            self.curr_dialogue.start_letterbyletter()
            self.dialogue_stack.append(temp)

        #if in the middle of a dialogue, a new one comes up
        if self.avatar_stack and self.curr_avatar != None:
            temp = self.curr_avatar
            self.curr_avatar = self.avatar_stack.pop()
            self.avatar_stack.append(temp)

        '''       
        #if in the midst of a new avalogue, a new one comes up that hasn't been used
        if self.avalogue_stack and self.curr_avalogue != None and not (self.avalogue_stack[0])[1].queue_flag:
            self.curr_avalogue[1].pause_letterbyletter()
            if self.curr_avalogue[1].button_num != 0:
                self.d_view.disable_buttons(self.curr_avalogue[1].button_num)
            temp = self.curr_avalogue
            self.curr_avalogue = self.avalogue_stack.pop()
            self.curr_avalogue[1].start_letterbyletter()
            self.avalogue_stack.append(temp)

        '''
        #If the current dialogue is not finished (it is showing as well)
        if self.curr_dialogue is not None and not self.curr_dialogue.finished:
            self.d_view.set_sentence(self.curr_dialogue.shown_text)
      
         #if a dialogue is running
        if self.curr_avatar != None:
            img = self.curr_avatar.get_currimage()
            self.a_view.set_image(img)

        '''
        if self.curr_avalogue is not None and self.curr_avalogue[1].showing:
            if self.curr_avalogue[1].queue_flag and not self.curr_avalogue[1].showing:
                print("should enable buttons!")
                self.d_view.enable_buttons(self.curr_avalogue[1].button_num)
            self.d_view.set_sentence(self.curr_avalogue[1].shown_text)
            img = self.curr_avalogue[0].get_currimage()
            self.a_view.set_image(img)
            

        '''
        #If dialogue is done showing and waiting for buttons (avatars should be idle this time)
        if self.curr_dialogue is not None and not self.curr_dialogue.showing:
            self.view.enable_buttons(self.curr_dialogue.button_num)
        
        #if the current dialogue is finished
        if self.curr_avatar != None and self.curr_avatar.finished:
            self.curr_avatar = None
        '''
        if self.curr_avalogue is not None and not self.curr_avalogue[1].showing and not self.curr_avalogue[0].finished:
            self.d_view.set_sentence(self.curr_avalogue[1].shown_text)     
            img = self.curr_avalogue[0].get_currimage()
            self.a_view.set_image(img)       
            if self.curr_avalogue[1].button_num != 0:
                self.d_view.enable_buttons(self.curr_avalogue[1].button_num)
                new_avalogue = (self.idle_avatar, self.curr_avalogue[1])
                self.curr_avalogue = new_avalogue

        
        
        '''
         #if the current dialogue is finished (for non-button mode, it's wiped actually) , Avatar should be idle here
        if self.curr_dialogue is not None and self.curr_dialogue.finished:
            self.curr_dialogue = None
        
        #if the current dialogue is finished
        if self.curr_avatar != None and self.curr_avatar.finished:
            self.curr_avatar = None
        '''
        #if the current dialogue is finished (for non-button mode, it's wiped actually), Avatar should be idle here
        if self.curr_avalogue is not None and self.curr_avalogue[1].finished:
            self.curr_avalogue = None
        

        '''
        #if the current dialogue is finished (for button mode) 
        if self.button_press:
            self.view.hide_buttons(self.curr_dialogue.button_num)
            func = utils.find_func(self.btn_press_name)
            print(func)
            self.curr_dialogue = None
            self.button_press = False
            self.btn_press_name = None
            func()
        #if the current dialogue is finished
        if self.curr_avatar != None and self.curr_avatar.finished:
            self.curr_avatar = None

        '''
        if self.button_press:
            self.d_view.hide_buttons(self.curr_avalogue[1].button_num)
            func = utils.find_func(self.btn_press_name)
            self.curr_avalogue = None
            self.button_press = None
            self.btn_press_name = None
            func()

        Tk.after(self.frame, 100, self.update_loop)
       
        
        

       

    def set_avalogue(self, a_key, d_key):
        
        avatar_obj  = self.a_model.find_obj(a_key)

        dialogue_obj = self.d_model.find_obj(d_key)
        
        self.d_view.init_buttons(dialogue_obj.button_num, 
                               dialogue_obj.button_title,
                                dialogue_obj.button1_title,
                                dialogue_obj.button2_title)
        
        self.avalogue_stack.append((avatar_obj, dialogue_obj))
        

        
        

        