# Mon Nov 13 11:01:17 PM PST 2023

New data colletion challenge: `pyautogui.screenshot` takes an average of 0.25 sec and `pyautogui.locateCenterOnScreen` takes 0.31 sec.

---
> endlog - Mon Nov 13 11:03:09 PM PST 2023

## Mon Nov 13 10:39:49 PM PST 2023

I want to enable standard training with stable baselines because it is nice to have our environmnet compatible with common RL and other algorithms. On the other hand, [it is known](https://benjaminwarner.dev/2022/08/31/training-atari-agents-faster) that sb3 is not very efficient with their buffers. Specifically, they pass data from gpu to cpu and back alot. In addition, at the moment of this log, their vectorized environment sampling is broken.

Regardless of sb3, having a gym interface is still useful, though additional research into how to do it right with realtime environments would be useful. [rtgym](https://pypi.org/project/rtgym/) is one option that we could use to build on top of.

Picking between synchronous vs asynchronous action taking question becomes harder in this case, because the `__call__` has to return something. If we want the action to be associated with the passed observation, it has to be blocking. This potentially slows us down, as the asynchronous version could otherwise pipeline actions.

gymmifying the interace will also enalbe us to sample from multilpe environmnets concurrently in the future. One challenge with this will be enabeling multiple mouse position inputs. Hoping that selenium driver enables multiple concurrent session interactions with a mouse.

---
> endlog - Mon Nov 13 10:53:08 PM PST 2023

## Sun Oct 29 07:16:29 PM PDT 2023

Trying to use pytesseract for text detection. It often fails by either missing one of the digits in food eaten, or confuses 0 for 9 in cells eaten.

---
> endlog - Sun Oct 29 07:22:21 PM PDT 2023

## Sat Oct 21 10:57:07 PM PDT 2023

There is a nice utilize for getting the agario windows and mac - `pygetwindow`.
It doesn't work no linux. Unfortunately, ubuntu is not as cooperative in window management.
GPT4 recommended using a 3rd party window utility libraries and interfacing with those through
the subprocess terminal. This will work as a termporary hack, but would be nice to have a solution that doesn't require you to install extra soft.

Decided to use `wmctrl` for now.

Thinking that at the moment the only thing that needs to happen in a thread is bot action. The data collection can then remain in the main thread. 

---
> endlog - Sat Oct 21 11:19:11 PM PDT 2023

## Fri Oct 20 10:25:24 PM PDT 2023

Possible problems with recording and playing bot:
 * the dt should be consistent between the recorder and player bot. This will be harder for different bots where more/less time is needed for a forward pass. How do we 1. guarantee that the player_bot is on time, 2. the recorded action-state touples are consitent with player?
 
Options:
1. define the dt and a deadline. Throw if its not met.
2. Incorporate dt into a state, make the model work with different cycle lengths. I imagine this complicates RL significantly because the dynamics are non-linear. The optimal policy would need to learn how to operate optimally at the whole range of dt[min-max]. Though maybe this could act as added noise for improving model generalization?

In terms of observation-action synchronization:
1. One state recorded per action. Take screenshot at the beginning, feed to dnn, wait for the end of the dt, execute the action and take a screenshot.    
This one can be done without threading, as the model is always waiting for the current state in the beginning of the cycle and no additional states are captured during the cycle.
2. N state recordings per model action. This could be helpufl if we have several offline rl models, some of which take longer than others, but we still want to utilize the data.    
In that case we want to keep the recording at a certain fps and the bot is independent. We also want to record as dense as possible, and we need threads.

---
> endlog - Fri Oct 20 11:08:52 PM PDT 2023

## Fri Oct 20 09:54:55 PM PDT 2023

I don't vim, so I updated log.sh to enable different editors. 
vladded current dev todos: enable parallel bot execution at all times and switching from bot to manual
Noticed eralier that the mouse position updates ignore the mouse delay and teleport to new positions instead of getting there in specified time.

Somewhat furhter down the line: 
 * see if hd5 numpy storage is better than a mighty .png pile in terms of storage.
 * parse the game over screen for reward information.
 * The current pixel-by-pixel button image detection is bad. MB train a simple CNN, or find some simple way of making kernels that can accurately detect the button 
regardless of the screen resolution, aspect ratio, etc.
---
> endlog - Fri Oct 20 10:08:52 PM PDT 2023

#