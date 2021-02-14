from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk 

root = Tk()
root.title('STARK INDUSTRIES - MUSIC PLAYER')
root.iconbitmap = (r'/Users/hardik/Desktop/Python/Music Player')
root.geometry("500x450")
song_length=None



#Initialize pygame mixer
pygame.mixer.init()


#Grab song length time info
def play_time():
    global song_length

    #Grab current song elapsed time
    current_time=pygame.mixer.music.get_pos() /1000
    
    #throw up temp label to get data
    slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos :{int(current_time)} ')
    
    
    #convter to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    #Get currently  playing song
    current_song = song_box.curselection()
    
    song = song_box.get(current_song)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"
    
    #load song length with mutagen
    song_mut = MP3(song)
    #Get song length
    song_length = song_mut.info.length

    #convert to time format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    my_slider.config(value=current_time)
    
    #increase current time by one second
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed:  {converted_song_length} ') 

    elif  int(my_slider.get()) == int(current_time):
        #Update Slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        #Update Slider to position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        #convter to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

        
        #output time to status bar
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length} ') 

        #move this thing along by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    
    #output time to status bar
    #status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length} ') 
    
    #update slider position value to current song postiton...
    #my_slider.config(value=int(current_time))
    '''fake_label=Label(root, text=int(current_time))
    fake_label.pack(pady=10)'''
    
    
    
    
    
    
    #update time
    status_bar.after(1000, play_time)

    
    #current_song = song_box.curselection()
    song = song_box.get(ACTIVE)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"
    
    
    #Get song length with mutagen
    song_mut = MP3(song)
    song_length = song_mut.info.length


    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    my_slider.config(value=current_time)
    








#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir = r'/Users/hardik/Desktop/Music', title = "Choose A Song",filetypes=(("mp3 Files","*.mp3 "), ))
    #print(song)

    #strip out the directory info and .mp3 extention
    song = song.replace("/Users/hardik/Desktop/Music/","")
    song = song.replace(".mp3","")
   
    #Add song to listbox
    song_box.insert(END, song)

#Add many songs
def add_many_songs():
     songs = filedialog.askopenfilenames(initialdir = r'/Users/hardik/Desktop/Music', title = "Choose A Song",filetypes=(("mp3 Files","*.mp3 "), ))

    #loop thorugh song list and replace directory info and mp3
     for song in songs:
        song = song.replace("/Users/hardik/Desktop/Music/","")
        song = song.replace(".mp3","")
        #insert into playlist
        song_box.insert(END, song)
        

#Play selected song
def play():
    song=song_box.get(ACTIVE)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Call the play_time function to get song lenght
    play_time()

    #Update Slider to position
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)





#stop playing current song
def stop():
     pygame.mixer.music.stop()
     song_box.selection_clear(ACTIVE)

     #clear the status bar
     status_bar.config(text='')

# Create global pause variable
global paused
paused= False



# Pause and unpause
def pause(is_paused):
    global paused
    paused=is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True


#create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song=song_box.get(ACTIVE)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#Play the next song in the playlist
def next_song():
    #get the current song tuple number
    next_one = song_box.curselection()
    #Add one to the next current song number
    next_one = next_one[0]+1
    song = song_box.get(next_one)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Move active bar in playlist listbox
    song_box.selection_clear(0, END)
    #Activate new song bar
    song_box.activate(next_one)

    #set active bar to next
    song_box.selection_set(next_one, last = None) 

#Play previous song in playlist
def previous_song():

    #get the current song tuple number
    next_one = song_box.curselection()
    #Add one to the next current song number
    next_one = next_one[0]-1
    song = song_box.get(next_one)
    song = f"/Users/hardik/Desktop/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Move active bar in playlist listbox
    song_box.selection_clear(0, END)
    #Activate new song bar
    song_box.activate(next_one)

    #set active bar to next
    song_box.selection_set(next_one, last = None) 


#Delete a song
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#Delete all songs from playlist
def delete_all_songs():
    song_box.delete(0, END)
    pygame.mixer.music.stop()



#creat playlist box
song_box = Listbox(root, bg="black", fg = "green", width = 50, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

#Create player control buttons images
back_btn_img = PhotoImage(file= r'/Users/hardik/Desktop/Python/Music Player/previous_50.png')
forward_btn_img = PhotoImage(file= r'/Users/hardik/Desktop/Python/Music Player/next_50.png')
play_btn_img = PhotoImage(file= r'/Users/hardik/Desktop/Python/Music Player/play_50.png')
pause_btn_img = PhotoImage(file= r'/Users/hardik/Desktop/Python/Music Player/pause_50.png')
stop_btn_img = PhotoImage(file= r'/Users/hardik/Desktop/Python/Music Player/stop_50.png')


# create player control frame
controls_frame = Frame(root)
controls_frame.pack()




# create player control images
back_btn = Button(controls_frame, image=back_btn_img, borderwidth = 0, command= previous_song)
forward_btm = Button(controls_frame, image=forward_btn_img , borderwidth = 0, command=next_song)
play_btn = Button(controls_frame, image=play_btn_img , borderwidth = 0, command=play)
pause_btn =Button(controls_frame, image= pause_btn_img, borderwidth = 0, command=lambda: pause(paused))
stop_btn = Button(controls_frame, image= stop_btn_img, borderwidth = 0, command=stop)

back_btn.grid(row = 0, column =0,padx = 10)
forward_btm.grid(row = 0, column =1,padx = 10) 
play_btn.grid(row = 0, column =2,padx = 10)
pause_btn.grid(row = 0, column =3,padx = 10)
stop_btn.grid(row = 0, column =4,padx = 10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add songs menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

#Add many songs to playlist
add_song_menu.add_command(label="Add Many Song To Playlist", command=add_many_songs)



#Create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Remove Songs", menu =remove_song_menu )
remove_song_menu.add_command(label = "Delete A Song From Playlist", command= delete_song)
remove_song_menu.add_command(label = "Delete All Song From Playlist", command = delete_all_songs)


#Create status bar
status_bar = Label(root, text='', bd=1,relief=GROOVE, anchor=E)
print(type(status_bar))
status_bar.pack(fill=X,ipady=2, side=BOTTOM)
 

#create music position slider
my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length= 360)
my_slider.pack(pady=30)


#create temporary slider label
slider_label = Label(root, text="0")
slider_label.pack(pady=10)




root.mainloop()
  