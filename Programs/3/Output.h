#ifndef OUTPUT_H
#define OUTPUT_H

#include <string>

template<typename T>
class Output {
public:
    virtual ~Output(){}
    virtual void write(const T&) = 0;
    virtual void writeString(const std::string&) = 0;
};

#endif

