#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import curses
import select

def main(stdscr, host):
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    # Color pairs
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    received = 0
    explicit_lost = 0
    start_time = time.time()

    # Start ping: -i 1 means one packet per second
    cmd = ["ping", "-i", "1", host]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        while True:
            # 1. Check User Input
            if stdscr.getch() == ord('q'):
                break

            # 2. Check if process died
            status = process.poll()
            if status is not None:
                break

            # 3. Read output (Non-blocking)
            r, _, _ = select.select([process.stdout], [], [], 0.05)
            if r:
                line = process.stdout.readline()
                if line:
                    line_lower = line.lower()
                    if "icmp_seq=" in line_lower:
                        if "time=" in line_lower:
                            received += 1
                        elif any(err in line_lower for err in ["timeout", "unreachable", "failed"]):
                            explicit_lost += 1

            # 4. Calculate Stats based on TIME (Robustness Fix)
            elapsed = time.time() - start_time
            sent = max(1, int(elapsed))
            
            # The Absolute Loss Counter:
            # We take the higher of (explicitly seen errors) or (the total deficit).
            # This prevents the loss count from decreasing when the connection returns.
            loss_count = max(explicit_lost, sent - received)
            loss_pct = (loss_count / sent * 100) if sent > 0 else 0.0
            
            # 5. Render UI
            stdscr.erase()
            h, w = stdscr.getmaxyx()
            
            # Header
            stdscr.addstr(0, 0, f" HOST: {host} ".center(w), curses.A_REVERSE | curses.A_BOLD)
            stdscr.addstr(1, 0, f" [Press 'q' to quit] ".rjust(w), curses.A_DIM)
            
            # Stats
            stdscr.addstr(3, 2, f" Time Elapsed:     {elapsed:.1f}s".ljust(w-4))
            stdscr.addstr(4, 2, f" Total Sent:       {sent}".ljust(w-4))
            stdscr.addstr(5, 2, f" Total Received:   {received}".ljust(w-4))
            stdscr.addstr(6, 2, f" Total Lost (Abs):  {loss_count}".ljust(w-4))
            
            # Loss and Color
            if loss_pct == 0:
                attr = curses.color_pair(1)
                msg = f" Loss %:          {loss_pct:.1f}%"
            elif loss_pct < 15:
                attr = curses.color_pair(2)
                msg = f" Loss %:          {loss_pct:.1f}% (Warning)"
            else:
                attr = curses.color_pair(3)
                msg = f" Loss %:          {loss_pct:.1f}% (CRITICAL!)"
                
            stdscr.addstr(8, 2, msg, attr)

            # Progress Bar
            bar_width = w - 10
            if bar_width > 5:
                filled = int((loss_pct / 100) * bar_width) if bar_width > 0 else 0
                if filled > bar_width: filled = bar_width
                bar_str = "|" + ("#" * filled) + ("-" * (bar_width - filled)) + "|"
                stdscr.addstr(10, 2, bar_str)

            stdscr.addstr(h-2, 0, " ═══ Monitor active ═══ ".center(w), curses.A_DIM)
            stdscr.refresh()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()
        try:
            process.wait(timeout=1)
        except:
            process.kill()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    try:
        curses.wrapper(lambda stdscr: main(stdscr, target))
    except Exception as e:
        print(f"Monitor exited: {e}")
