import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


class Arrvis:
    """An array visualizer class. Passing in an array to the init is optinal.
    another optional parameter is the boolean plot variable.
    This controls whether the animation is updated in real time
    """

    def __init__(self, arr=[], plot=False):
        self.arr = list(arr)
        self.frames = [(arr, [], "w")]
        self.plot = plot
        self.titles = {}
        self.curr_title = ""
        """ this object will hold a list of the frames needed for plotting
            each frame will hold 
                a) the current list after an operation is completed
                b) the index (indicies) being operated upon
                c) a color depending on the operation 
                    read = deepskyblue
                    write = red
                    swap = darkviolet
        """
        if self.plot:
            plt.style.use("dark_background")
            self.dom = np.arange(len(arr))
            plt.ion()
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
            self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.rect_container = plt.bar(self.dom, self.arr, color="w")
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            # self.fig.show()

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, idx):
        return self.read(idx)

    def __setitem__(self, idx, val):
        self.write(idx, val)

    def change_title(self, title):
        self.titles[len(self.frames)] = title
        if self.plot:
            self.ax.set_title(title)
        self.curr_title = title

    def append_frame(self, idxs, color):
        # [print(i) for i in self.arr]
        deepcopy = [i for i in self.arr]
        self.frames.append((deepcopy, idxs, color))

        if self.plot:
            prev_vals = self.frames[-2][0]
            prev_idxs = self.frames[-2][1]

            diff_idxs = np.where(np.equal(self.arr, prev_vals) == False)[0]

            # self.fig.canvas.restore_region(self.background)

            for i, rect in enumerate(self.rect_container):
                is_changed = False
                if i in prev_idxs:
                    rect.set(color="w")
                    is_changed = True
                if i in idxs:
                    rect.set(color=color)
                    is_changed = True
                if i in diff_idxs:
                    rect.set_height(self.arr[i])
                self.ax.draw_artist(rect)
            self.fig.canvas.blit(self.ax.bbox)
            # self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            # plt.pause(1/len(self.arr)**2)

            self.frames = self.frames[-2:]

    def read(self, idx):
        self.append_frame([idx], "deepskyblue")
        return self.arr[idx]

    def write(self, idx, val):
        self.arr[idx] = val
        self.append_frame([idx], "red")

    def swap(self, idx1, idx2):
        self.arr[idx1], self.arr[idx2] = self.arr[idx2], self.arr[idx1]
        self.append_frame([idx1, idx2], "darkviolet")

    def verify(self):
        old_title = self.curr_title
        self.change_title("verifying...")
        issorted = True
        for i in range(len(self) - 1):
            if self.arr[i] <= self.arr[i + 1]:
                self.append_frame([j for j in range(i)], "lime")
            else:
                issorted = False
                break
        if issorted:
            self.change_title("success!")
            num_frames = min(len(self), 50)
            c = "lime"
        else:
            self.change_title("sort failed!")
            num_frames = min(len(self), 50) * 2
            c = "r"
        for i in range(num_frames):
            self.append_frame([j for j in range(len(self))], c)
        self.change_title(old_title)

    def clear_frames(self):
        self.frames.clear()

    def animate_frames(self, filename="multisort", ms_frame=None, video_length=60):
        if self.plot:
            plt.close(self.fig)
        self.append_frame([], "k")
        self.append_frame([], "k")
        plt.style.use("dark_background")
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim(0, np.max(self.arr) + 1)
        ax.set_title(f"sorting")

        full_frame_0 = self.frames[0][0]
        rect_container = ax.bar(range(len(full_frame_0)), full_frame_0, color="w")

        def update(i):
            if i == 0:
                return rect_container
            if i in self.titles:
                ax.set_title(self.titles[i])
            # change previous indicies back to white
            prev_vals = self.frames[i - 1][0]  # previous values of the array
            prev_idxs = self.frames[i - 1][1]  # previous idxs that were colored
            curr_vals = self.frames[i][0]  # current values of the array
            curr_idxs = self.frames[i][1]  # current idxs that need to be colored
            color = self.frames[i][2]  # current color that needs to be colored

            diff_idxs = np.where(np.equal(prev_vals, curr_vals) == False)[0]
            changed = []

            for i, rect in enumerate(rect_container):
                is_changed = False
                if i in prev_idxs:
                    rect.set(color="w")
                    is_changed = True
                if i in curr_idxs:
                    rect.set(color=color)
                    is_changed = True
                if i in diff_idxs:
                    rect.set_height(curr_vals[i])
                    is_changed = True
                if is_changed:
                    changed.append(rect)

            return changed

        if ms_frame is None:
            ms_frame = 1000 * video_length / len(self.frames)

        anim = animation.FuncAnimation(
            fig, update, frames=range(len(self.frames)), interval=ms_frame, blit=True
        )
        # plt.show()
        start_time = time.time()
        print(f"animating {len(self.frames)} frames")
        anim.save(
            f"{filename}.mp4",
            progress_callback=lambda i, n: print(
                f"  {100*((i+1)/n):.3f}% eta: {(time.time()-start_time)*((n-i)/(i+1)):.0f} sec   ",
                end="\r",
            ),
        )
        print(f'animation saved to "{filename}.mp4"')
