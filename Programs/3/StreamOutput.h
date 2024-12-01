#ifndef STREAM_OUTPUT_H
#define STREAM_OUTPUT_H

#include "Output.h"
#include <iostream>

template<typename T>
class StreamOutput : public Output<T> {
    std::ostream& sink;
public:
    explicit StreamOutput(std::ostream& stream) : sink(stream) {}
    void write(const T& t) {
        sink << t;
    }
    void writeString(const std::string& s) {
       sink << s;
    }
};

#endif

