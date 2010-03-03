from  sys import platform, byteorder
import thread
from translation import _
# sonar.wav: thanks to Partners In Rhyme (www.partnersinrhyme.com)
# source code: thanks to Bill Dandreta (in  www.velocityreviews.com 2004-10-23)



def play(soundfile):
    thread.start_new_thread(_play, (soundfile,))

def _play(soundfile):
    if platform.startswith('win'):
        from winsound import PlaySound, SND_FILENAME, SND_ASYNC
        PlaySound(soundfile, SND_FILENAME|SND_ASYNC)
    elif 'linux' in platform:
        from wave import open as waveOpen
        from ossaudiodev import open as ossOpen
        
        s = waveOpen(soundfile,'rb')
        (nc,sw,fr,nf,comptype, compname) = s.getparams( )
        
        try:
            from ossaudiodev import AFMT_S16_NE
        except ImportError:
            if byteorder == "little":
                AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
            else:
                AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
        
        dsp = None
        try:
            dsp = ossOpen('/dev/dsp','w')
            dsp.setparameters(AFMT_S16_NE, nc, fr)
            data = s.readframes(nf)
            s.close()
            dsp.write(data)
        except IOError:
            print _("Audio device is busy.")
        finally:
            if dsp:
                dsp.close()
     