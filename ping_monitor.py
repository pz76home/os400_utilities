#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import curses
import select

def main(stdscr, host):
    """Main curses loop for monitoring connectivity."""
    curses.curs_set(0)
    stdscr.nodelay(True)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    sent = 0
    received = 0
    lost = 0

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
            key = stdscr.getch()
            if key == ord('q'):
                break

            status = process.poll()
            if status is not None:
                break

            r, _, _ = select.select([process.stdout], [], [], 0.05)
            if r:
                line = process.stdout.readline()
                if line:
                    if "icmp_seq=" in line:
                        sent += 1
                        if "time=" in line:
                            received += 1
                    elif "timeout" in line.lower() or "unreachable" in line.lower():
                        sent += 1
                        lost += 1

            total_attempted = sent
            loss_pct = (lost / total_attempted * 100) if total_attempted > 0 else 0.0

            stdscr.erase()
            h, w = stdscr.getmaxyx()

            stdscr.addstr(0, 0, f" HOST: {host} ".center(w), curses.A_REVERSE | curses.A_BOLD)
            stdscr.addstr(1, 0, f" [Press 'q' to quit] ".rjust(w), curses.A_DIM)

            stdscr.addstr(3, 2, f" Packets Sent:     {sent}".ljust(w-4))
            stdscr.addstr(4, 2, f" Packets Received: {received}".ljust(w-4))

            if loss_pct == 0:
                attr = curses.color_pair(1)
            elif loss_pct < 10:
                attr = curses.color_pair(2)
            else:
                attr = curses.color_pair(3)

            stdscr.addstr(6, 2, f" Packet Loss:      {loss_pct:.1f}%", attr)

            bar_width = w - 10
            if bar_width > 5:
                filled = int((loss_pct / 100) * bar_width)
                if filled > bar_width: filled = bar_width
                bar_str = "|" + ("#" * filled) + ("-" * (bar_width - filled)) + "|"
                stdscr.addstr(8, 2, bar_str)
                stdscr.addstr(9, 2, " [Higher is Worse]".ljust(w-4), curses.A_DIM)

            stdscr.addstr(h-2, 0, " ═══ Monitor active ═══ ".center(w), curses.A_DIM)
            stdscr.refresh()
            time.sleep(0.05)

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
