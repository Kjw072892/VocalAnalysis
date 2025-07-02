import parselmouth
import math
import numpy as np
import tkinter as tk
from tkinter import Tk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


"""
Output the collected data for easy use

The first list added will be designated as F0, the second F1 and so on
list[float] [f0, f1, f2, f3, f4]
"""
def output(*args: list[float], list_times:list[list[float]]):

    window = tk.Tk()
    window.geometry("650x1050")
    window.title("Vocal Analysis Report")
    window.resizable(False, False)


    canvas = tk.Canvas(window,width=620, height=550)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.config(width=620,height=550)
    canvas.create_window((0,0), window=scroll_frame, anchor="nw")

    formant_tuple = []

    pitch_explain = """
* Cis Women pitch range: [165 - 255] Hz -> Averaging ~210 Hz
    
* Cis Men pitch range: [85 - 155] Hz -> Averaging ~120 Hz
    
* Falsetto (Cis Men): [~200 - 350] Hz
"""

    average_text = ""

    lowest_text = ""

    highest_text = ""

    result_explain = """    
* Formant [F1-F4] are frequency ranges of vowel's formant. 
* Vowels and vocal-tract-shape influences your formant frequencies.
* Bellow are typical formant ranges of Cisgender Women and Cisgender Men.
* Formant data can give you a good idea about how you are forming your
  vowels, tongue placements, lips placements, jaw placements, 
  and resonance locations

* Tongue Height (Jaw Opening):

    ** F1: Cis Women [310 - 860] Hz | Cis Men [270 - 730] Hz 
    
    - High tongue (closed mouth) -> Low F1
        + Vowels like /i/("ee" as in beet), /u/("00" in boot)
        
    - Low tongue (open mouth) -> High F1
        + Vowels like /a/("ah" in father), /æ/("a" in cat)
        
    - Inversely related to tongue height 

* Tongue Frontness:

    ** F2: Cis Women [920 - 2790] Hz | Cis Men [870 - 2290] Hz
    
    - Tongue forward -> High F2
        + Vowels like /i/("ee"), /e/("ay")
        
    - Tongue back -> Low F2
        + Vowels like /u/ ("oo"),/o/ ("oh", /a/("aw")
    
    - Directly related to tongue front-ness

* Lip Shape & Resonance Characteristics:

    ** F3: Cis Women [2670 - 3300] Hz | Cis Men [2240 - 3010] Hz 
     
    - Influenced by:
        + Lip rounding -> Lowers F3 (as in /r/ and /u/)
        + Constrictions in oral cavity
    
    - Less dramatically tied to vowels than F1/F2, but:
        + /i/ tends to have high F3
        + /u/ and /r/ have low F3

* Speaker & Timbre Characteristics:

    ** F4: Cis Women [3300 - 4000+] Hz | Cis Men [3000 - 3700] Hz
    
    - Not directly vowel-diagnostic
    
    - Affected by:
        + Vocal tract length
        + Voice quality
        + Subtle articulation cues
    
    - Used more in voice profiling (e.g., gender, vocal effort), 
      not vowel identification
"""

    result_text = ""

    for freq_list in args:
        formant_tuple.append(freq_list)

    for i, freqs in enumerate(formant_tuple):
        if i == 0:
            average_text += f"Pitch Average: {get_freq_average(freqs):0.2f} Hz\n"
        else:
            average_text += f"F{i} Average: {get_freq_average(freqs):0.2f} Hz\n"
    lowest = []
    highest = []
    for i, freqs in enumerate(formant_tuple):
        freq_sorted = sorted(freqs)
        lowest.append(freq_sorted[i])
        highest.append(freq_sorted[len(freqs) - 1])

    for i in range(0, len(lowest)):
        lowest_text += f"F{i}: {lowest[i]: 0.2f} Hz\n"

    for i in range(0, len(highest)):
        highest_text += f"F{i}: {highest[i]: 0.2f} Hz\n"

    result_text += f"""
Your lowest Pitch is: [{lowest[0]:0.0f} Hz]; Your highest Pitch is [{highest[0]:0.0f} Hz]\n
"""
    is_within_cis_women_pitch_range = 165 < get_freq_average(formant_tuple[0]) < 400
    is_within_cis_men_pitch_range = 92 <=  get_freq_average(formant_tuple[0]) < 145
    is_androgynous_pitch = 145 <= get_freq_average(formant_tuple[0]) <= 165

    if is_within_cis_women_pitch_range:
        result_text += "    - Your pitch-average is within cis women's average pitch-range\n"
    elif is_within_cis_men_pitch_range:
        result_text += "    - Your pitch-average is within cis men's average pitch range\n"
    elif is_androgynous_pitch:
        result_text += "    - Your pitch-average lies within the androgynous zone. \n"


    # TODO: Display results for the formant data

    label_header = tk.Label(scroll_frame, text="Vocal Analysis Tool-Kit", justify="left", anchor="w",font=("Ariel",20))
    label_header.pack(padx=0, pady=5, anchor="w")

    label_pitch_explain = tk.Label(scroll_frame, text=pitch_explain, justify="left", anchor="w", font=("Ariel", 10))
    label_pitch_explain.pack(padx=0, pady=5, anchor="w")

    label_average = tk.Label(scroll_frame, text="Average (yours): ", justify="left", anchor="w", font=("Ariel", 20))
    label_average.pack(padx = 0, pady = 5, anchor="w")

    label_average1 = tk.Label(scroll_frame, text=average_text, justify="left", anchor="w", font=("Ariel", 10))
    label_average1.pack(padx=0, pady=20, anchor="w")

    label_lowest = tk.Label(scroll_frame, text="Lowest Frequencies (yours):", justify="left", anchor="w",
                            font=("Ariel", 20))
    label_lowest.pack(padx=0, pady=5, anchor="w")

    label_lowest1 = tk.Label(scroll_frame, text=lowest_text, justify="left", anchor="w", font=("Ariel", 10))
    label_lowest1.pack(padx=0, pady=20, anchor="w")

    label_highest = tk.Label(scroll_frame, text="Highest Frequencies (yours): ", justify="left", anchor="w",font=("Ariel", 20))
    label_highest.pack(padx=0, pady=5, anchor="w")

    label_highest1 = tk.Label(scroll_frame, text=highest_text, justify="left", anchor="w", font=("Ariel", 10))
    label_highest1.pack(padx=0, pady=20, anchor="w")

    label_result_tag = tk.Label(scroll_frame, text = "Formant Information:", justify="left",
     anchor="w", font=("Ariel", 20))
    label_result_tag.pack(padx=0, pady=5, anchor="w")

    label_result = tk.Label(scroll_frame, text=result_explain, justify="left", wraplength=600, anchor="w",font=("Ariel", 10))
    label_result.pack(padx=0, pady=5, anchor="w")

    label_result_ = tk.Label(scroll_frame, text="Formant/Pitch Result:", justify="left", anchor="w", font=("Ariel", 20))
    label_result_.pack(padx=0, pady=5, anchor="w")

    # Embedding the scatter plot
    fig = Figure(figsize=(6, 12), dpi=100)
    ax = fig.add_subplot(111)
    max_freqs = max(max(f0_vals_arr), max(f1_vals_arr), max(f2_vals_arr), max(f3_vals_arr), max(f4_vals_arr))

    ax.plot(list_times[0], f0_vals_arr, label='Pitch', color='black')
    ax.scatter(list_times[1], f1_vals_arr, label='F1')
    ax.scatter(list_times[2], f2_vals_arr, label='F2')
    ax.scatter(list_times[3], f3_vals_arr, label='F3')
    ax.scatter(list_times[4], f4_vals_arr, label='F4')

    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_yticks(list(np.arange(0, 1001, 100)) + list(np.arange(1100, max_freqs, 200)))
    ax.set_title("Formant Tracks Over Time")
    ax.legend()
    ax.grid(True)

    canvas_plot = FigureCanvasTkAgg(fig, master=scroll_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(padx=10, pady=10, anchor="e")
    canvas.pack(side="left", fill="both", expand=False)


    #TODO: add analysis label and three buttons on the bottom [woman, man, non-binary]

    label_result1 = tk.Label(scroll_frame, text=result_text, justify="left", anchor="w", font=("Ariel", 10))
    label_result1.pack(padx=0, pady=5, anchor="w")



    def on_close():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    window.resizable(None, None)
    try:
         window.mainloop()
    except KeyboardInterrupt:
        print("Program Closed")



"""
Filters anomalous frequencies

time_list: A list of the time stamp extracted from the audio sample
freqs: A list of the frequencies extracted from the audio sample

returns: tuple with the new synchronized time stamp and a list of the filtered frequencies
"""
def filter_frequency_synchronized(formant_: str, time_list: list[float], freqs: list[float]) -> tuple[list[float], list[float]]:

    # First Filter
    new_times = []
    new_freqs = []

    for time, freq in zip(time_list, freqs):

        if freq > 0:
            new_times.append(time)
            new_freqs.append(freq)

    # Second Filter low/high pass filter

    prev_freq = 0

    temp_freq = []
    temp_time = []

    for time, freqs in zip(new_times, new_freqs):

        if prev_freq == 0:
            prev_freq = freqs
            continue
        if formant_.casefold() == "f0":
            if 60 < freqs < 335:
                temp_freq.append(freqs)
                temp_time.append(time)
                prev_freq = freqs
                continue
        elif formant_.casefold() == "f1":
            if 250 <= freqs < 890:
                temp_freq.append(freqs)
                temp_time.append(time)
                prev_freq = freqs
                continue
        elif formant_.casefold() == "f2":
            if 800 <= freqs < 2800:
                temp_freq.append(freqs)
                temp_time.append(time)
                prev_freq = freqs
                continue
        elif formant_.casefold() == "f3":
            if 2000 < freqs < 3400:
                temp_freq.append(freqs)
                temp_time.append(time)
                prev_freq = freqs
                continue
        elif formant_.casefold() == "f4":
            if 2800 < freqs < 4500:
                temp_freq.append(freqs)
                temp_time.append(time)
                prev_freq = freqs
                continue

    new_times = temp_time
    new_freqs = temp_freq

    return new_times, new_freqs


"""
Get the average frequency for the designated formant frequency band

freq_data: list of frequencies extracted from the sample
sel_formant: the formant frequency band( F0, F1, F2, F3, F4)
"""
def get_freq_average(freq_data: list[float]):
    result = 0
    num_of_freq = 0

    for freq in freq_data:
        result += freq
        num_of_freq += 1

    return result / num_of_freq


"""
Gets the lowest Formant in the dataset

arr: the array with the formant dataset

formant_low: F0 - F4
"""
def get_low(freq_data: list[float], formant_low: str):
    low = freq_data[0]

    min_freq = 0

    match formant_low.casefold():
        case "F0":
            min_freq = 91
        case "F1":
            min_freq = 250
        case "F2":
            min_freq = 600
        case "F3":
            min_freq = 1500
        case "F4":
            min_freq = 2500

    for index in range(0, len(freq_data)):
        low = freq_data[index] if low > freq_data[index] > min_freq else low

    return low


"""
Gets the highest Formant in the data set

: the array with the formant dataset

formant_high: F0 - F4
"""
def get_high(freq_data: list[float], formant_high: str):
    high = freq_data[0]
    high_freq = 0

    match formant_high.casefold():
        case "F0":
            high_freq = 650
        case "F1":
            high_freq = 900
        case "F2":
            high_freq = 2500
        case "F3":
            high_freq = 3400
        case "F4":
            high_freq = 4500

    for index in range(0, len(freq_data)):
        high = freq_data[index] if high < freq_data[index] < high_freq else high

    return high

file_path = None  # Global so it can be used by the rest of your script
root = tk.Tk()
root.title("Select Audio File")
root.geometry("400x150")
root.resizable(False, False)

def exit_app():
    root.destroy()

def get_file_path():
    global file_path
    file_path = filedialog.askopenfilename(title="Select an Audio File")
    if file_path:
        root.destroy()  # Close the window to continue the main script
    else:
        label.config(text="Please select a valid file!")

label = tk.Label(root, text="Please Select Your Audio File.",font=("Ariel", 11))
label.pack(side="top", anchor="center", pady=(30,30))

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=(10,30))

btn_width = 12


button = tk.Button(button_frame, text="Choose File", width=btn_width,command=get_file_path)
button.pack(side="left", padx= 10)

exit_button = tk.Button(button_frame, text="Exit", width=btn_width ,command=exit_app)
exit_button.pack(side="left", padx=10)

root.mainloop()


if file_path:
    sound = parselmouth.Sound(file_path)
    formant = sound.to_formant_burg(time_step=0.01)
    pitch = sound.to_pitch(time_step=0.01)

    times = np.arange(0, sound.get_total_duration(), .01)

    f0_dict = {}
    f1_dict = {}
    f2_dict = {}
    f3_dict = {}
    f4_dict = {}

    # Initializes the formant and pitch
    for t in times:
        f0 = pitch.get_value_at_time(t)
        f1 = formant.get_value_at_time(1, t)
        f2 = formant.get_value_at_time(2, t)
        f3 = formant.get_value_at_time(3, t)
        f4 = formant.get_value_at_time(4, t)

        if (not math.isnan(f0) and not math.isnan(f1) and not math.isnan(f2)
                and not math.isnan(f3) and not math.isnan(f4)):
            f0_dict[float(t)] = f0
            f1_dict[float(t)] = f1
            f2_dict[float(t)] = f2
            f3_dict[float(t)] = f3
            f4_dict[float(t)] = f4

    times = sorted(f1_dict.keys())

    f0_vals_arr = [round(f0_dict[t], 0) for t in times]
    f1_vals_arr = [round(f1_dict[t], 0) for t in times]
    f2_vals_arr = [round(f2_dict[t], 0) for t in times]
    f3_vals_arr = [round(f3_dict[t], 0) for t in times]
    f4_vals_arr = [round(f4_dict[t], 0) for t in times]

    #Filters out all the frequency anomalies
    times_f0, f0_vals_arr = filter_frequency_synchronized("F0", times,  f0_vals_arr)
    times_f1, f1_vals_arr = filter_frequency_synchronized("F1", times, f1_vals_arr)
    times_f2, f2_vals_arr = filter_frequency_synchronized("F2", times, f2_vals_arr)
    times_f3, f3_vals_arr = filter_frequency_synchronized("F3", times, f3_vals_arr)
    times_f4, f4_vals_arr = filter_frequency_synchronized("F4", times, f4_vals_arr)

    f0_average = get_freq_average(f0_vals_arr)
    f1_average = get_freq_average(f1_vals_arr)
    f2_average = get_freq_average(f2_vals_arr)
    f3_average = get_freq_average(f3_vals_arr)
    f4_average = get_freq_average(f4_vals_arr)

    #Get the lowest and highest frequencies
    f0_low, f0_high = get_low(f0_vals_arr, "f0".casefold()), get_high(f0_vals_arr, "f0".casefold())
    f1_low, f1_high = get_low(f1_vals_arr, "f1".casefold()), get_high(f1_vals_arr, "f1".casefold())
    f2_low, f2_high = get_low(f2_vals_arr, "f2".casefold()), get_high(f2_vals_arr, "f2".casefold())
    f3_low, f3_high = get_low(f3_vals_arr, "f3".casefold()), get_high(f3_vals_arr, "f3".casefold())
    f4_low, f4_high = get_low(f4_vals_arr, "f4".casefold()), get_high(f4_vals_arr, "f4".casefold())




def main():
    try:
        output(f0_vals_arr, f1_vals_arr, f2_vals_arr, f3_vals_arr, f4_vals_arr,
               list_times=[times_f0, times_f1, times_f2, times_f3, times_f4])

    except NameError:
        print("No File Selected")

if __name__ == "__main__":
    main()