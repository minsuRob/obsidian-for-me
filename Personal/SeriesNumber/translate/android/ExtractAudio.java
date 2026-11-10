import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import android.media.MediaCodec;
import java.nio.ByteBuffer;

public class ExtractAudio {
 public static void main(String[] args) throws Exception {
  if(args.length!=2) throw new IllegalArgumentException("Usage: input.mp4 output.m4a");
  MediaExtractor e=new MediaExtractor(); MediaMuxer m=null;
  try {
   e.setDataSource(args[0]); int track=-1; MediaFormat format=null;
   for(int i=0;i<e.getTrackCount();i++){MediaFormat f=e.getTrackFormat(i); if("audio/mp4a-latm".equals(f.getString(MediaFormat.KEY_MIME))){track=i;format=f;break;}}
   if(track<0) throw new IllegalStateException("AAC audio track not found; conversion required");
   e.selectTrack(track); m=new MediaMuxer(args[1],MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4); int out=m.addTrack(format); m.start();
   int size=format.containsKey(MediaFormat.KEY_MAX_INPUT_SIZE)?format.getInteger(MediaFormat.KEY_MAX_INPUT_SIZE):1048576;
   ByteBuffer b=ByteBuffer.allocateDirect(Math.max(size,1048576)); MediaCodec.BufferInfo info=new MediaCodec.BufferInfo(); long samples=0;
   while(true){b.clear();int n=e.readSampleData(b,0);if(n<0)break; info.set(0,n,e.getSampleTime(),e.getSampleFlags());m.writeSampleData(out,b,info);samples++;e.advance();}
   m.stop(); System.out.println("AAC samples="+samples+" format="+format);
  } finally {if(m!=null)m.release();e.release();}
 }
}
