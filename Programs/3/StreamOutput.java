import java.io.*;

class StreamOutput implements Output {
    private Writer sink;
    public StreamOutput(Writer stream) {
        sink = stream;
    }
    public void write(Object o) {
        writeString(o.toString());
    }
    public void writeString(String s) {
        try {
            sink.write(s);
        }
        catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}