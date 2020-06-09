import srt


def basic_error(input_subs, manual_subs, max_width=42):
    """Takes the generated subtitles and the manual subtitles and compares
    them. A caption group is considered to be correct if the last word of the
    caption group and the first word of the next are the same as in the manual
    subtitles. When max_width is exceeded we penalise the captiongroup. In the
    end this function is intended to be maximalised.

    takes:
    input_subs: the generated subtitles as a srt parsed list
    manual_subs: the man-made subtitles we considered to correct
    max_width: how long a caption is allowed to be, default 42

    outputs: amount of correctly created captiongroups, and amount of times
    max_width was exceeded
    """
    good = 0
    penalty = 0
    for i, (sub1, next_sub1) in enumerate(zip(input_subs, input_subs[1:])):
        for sub2, next_sub2 in zip(manual_subs[i:], manual_subs[i+1:]):
            if sub1.content.split(' ')[-1] == sub2.content.split(' ')[-1] and next_sub1.content.split(' ')[0] == next_sub2.content.split(' ')[0]:
                good += 1
                break

        if len(sub1.content) > max_width:
            penalty += 1

    return good, penalty


### EXAMPLE USAGE ###
input_subs = list(srt.parse('''\
1
00:00:00,240 --> 00:00:02,750
thanks to last past for sponsoring a portion of this video.

2
00:00:02,870 --> 00:00:03,880
More from them later.

3
00:00:04,030 --> 00:00:05,080
Ladies and gentlemen,

4
00:00:05,090 --> 00:00:08,360
we build a lot of high performance computers around here,

5
00:00:08,360 --> 00:00:10,550
but today is going to be different.

6
00:00:10,940 --> 00:00:17,560
We scoured the Internet for the slowest brand new components that money can buy,

7
00:00:17,630 --> 00:00:21,050
and we're gonna build it right here right now.

8
00:00:21,460 --> 00:00:22,780
Then for comparison.

9
00:00:22,860 --> 00:00:36,050
We also grab some sort of what I would consider to be budget components but sensible ones to see just how much more performance you can get if you balance your budget,

10
00:00:37,900 --> 00:00:39,250
it's really the packaging for that.

11
00:00:39,840 --> 00:00:41,160
We're gonna get to that bit later,

12
00:00:41,160 --> 00:00:41,490
though.

13
00:00:41,760 --> 00:00:43,350
First,

14
00:00:43,590 --> 00:00:43,970
don't worry,

15
00:00:44,390 --> 00:00:47,400
parts aren't in there already to throw that in joke.'''))

manual_subs = list(srt.parse('''\
1
00:00:00,370 --> 00:00:02,910
- Thanks to LastPass for
sponsoring a portion of this video.

2
00:00:02,910 --> 00:00:04,100
More from them later.

3
00:00:04,100 --> 00:00:06,260
Ladies and gentlemen, we build a lot

4
00:00:06,260 --> 00:00:08,390
of high-performance computers around here,

5
00:00:08,390 --> 00:00:11,050
but today is gonna be different.

6
00:00:11,050 --> 00:00:12,780
We scoured the Internet

7
00:00:12,780 --> 00:00:17,670
for the slowest brand new
components that money can buy,

8
00:00:17,670 --> 00:00:21,490
and we're gonna build it
right here, right now.

9
00:00:21,490 --> 00:00:25,230
Then for comparison, we also grabbed some

10
00:00:25,230 --> 00:00:28,490
sort of what I would consider
to be budget components,

11
00:00:28,490 --> 00:00:30,430
but sensible ones,

12
00:00:30,430 --> 00:00:33,850
to see just how much more
performance you can get

13
00:00:33,850 --> 00:00:36,223
if you balance your budget.

14
00:00:37,890 --> 00:00:40,060
Is that really the packaging for that?

15
00:00:40,060 --> 00:00:42,710
We're gonna get to that
a bit later, though.

16
00:00:42,710 --> 00:00:45,250
First, don't worry, the
parts aren't in there.

17
00:00:45,250 --> 00:00:46,100
It's already built.

18
00:00:46,100 --> 00:00:48,359
Let's roll that intro, tsk.'''))


if __name__ == '__main__':
    print(basic_error(input_subs, manual_subs))
