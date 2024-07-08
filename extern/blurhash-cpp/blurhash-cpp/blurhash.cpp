// https://github.com/Nheko-Reborn/blurhash
// Boost Software License - Version 1.0 - August 17th, 2003
//
// Permission is hereby granted, free of charge, to any person or organization
// obtaining a copy of the software and accompanying documentation covered by
// this license (the "Software") to use, reproduce, display, distribute,
// execute, and transmit the Software, and to prepare derivative works of the
// Software, and to permit third-parties to whom the Software is furnished to
// do so, all subject to the following:
//
// The copyright notices in the Software and this entire statement, including
// the above license grant, this restriction and the following disclaimer,
// must be included in all copies of the Software, in whole or in part, and
// all derivative works of the Software, unless such copies or derivative
// works are solely in the form of machine-executable object code generated by
// a source language processor.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
// SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
// FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
// ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

#include "blurhash.hpp"

#include <cmath>
#include <algorithm>
#include <array>
#include <cassert>
#include <stdexcept>

#define M_PI        3.14159265358979323846264338327950288

using namespace std::literals;

namespace {
    constexpr std::array<char, 84> int_to_b83{
            "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%*+,-.:;=?@[]^_{|}~"};

    std::string
    leftPad(std::string str, size_t len) {
        if (str.size() >= len)
            return str;
        return str.insert(0, len - str.size(), '0');
    }

    constexpr std::array<int, 255> b83_to_int = []() constexpr {
        std::array<int, 255> a{};

        for (int i = 0; i < 83; i++) {
            a[static_cast<unsigned char>(int_to_b83[i])] = i;
        }

        return a;
    }
            ();

    std::string
    encode83(uint value) {
        std::string buffer;

        do {
            buffer += int_to_b83[value % 83];
        } while ((value = value / 83));

        std::reverse(buffer.begin(), buffer.end());
        return buffer;
    }

    struct Components {
        uint x, y;
    };

    uint
    packComponents(const Components &c) noexcept {
        return (c.x - 1) + (c.y - 1) * 9;
    }

    Components
    unpackComponents(uint c) noexcept {
        return {c % 9 + 1, c / 9 + 1};
    }

    int
    decode83(std::string_view value) {
        int temp = 0;

        for (char c: value)
            if (b83_to_int[static_cast<unsigned char>(c)] < 0)
                throw std::invalid_argument("invalid character in blurhash");

        for (char c: value)
            temp = temp * 83 + b83_to_int[static_cast<unsigned char>(c)];
        return temp;
    }

    float
    decodeMaxAC(int quantizedMaxAC) noexcept {
        return static_cast<float>(quantizedMaxAC + 1) / 166.f;
    }

    float
    decodeMaxAC(std::string_view maxAC) {
        if (maxAC.size() != 1)
            throw std::invalid_argument("decode max AC value != 1");
        return decodeMaxAC(decode83(maxAC));
    }

    int
    encodeMaxAC(float maxAC) noexcept {
        return std::clamp(int(maxAC * 166 - 0.5f), 0, 82);
    }

    float
    srgbToLinear(uint8_t value) noexcept {
        auto srgbToLinearF = [](float x) {
            if (x <= 0.0f)
                return 0.0f;
            else if (x >= 1.0f)
                return 1.0f;
            else if (x < 0.04045f)
                return x / 12.92f;
            else
                return std::pow((x + 0.055f) / 1.055f, 2.4f);
        };

        return srgbToLinearF(static_cast<float>(std::clamp(static_cast<int>(value), 0, 255)) / 255.f);
    }

    uint8_t
    linearToSrgb(float value) noexcept {
        auto linearToSrgbF = [](float x) -> float {
            if (x <= 0.0f)
                return 0.0f;
            else if (x >= 1.0f)
                return 1.0f;
            else if (x < 0.0031308f)
                return x * 12.92f;
            else
                return std::pow(x, 1.0f / 2.4f) * 1.055f - 0.055f;
        };

        return std::clamp(static_cast<int>(std::round(linearToSrgbF(value) * 255.f + 0.5f)), 0, 255);
    }

    struct Color {
        float r, g, b;

        Color &operator*=(float scale) {
            r *= scale;
            g *= scale;
            b *= scale;
            return *this;
        }

        friend Color operator*(Color lhs, float rhs) { return (lhs *= rhs); }

        Color &operator/=(float scale) {
            r /= scale;
            g /= scale;
            b /= scale;
            return *this;
        }

        Color &operator+=(const Color &rhs) {
            r += rhs.r;
            g += rhs.g;
            b += rhs.b;
            return *this;
        }
    };

    Color
    decodeDC(int value) {
        const int intR = value >> 16;
        const int intG = (value >> 8) & 255;
        const int intB = value & 255;
        return {srgbToLinear(intR), srgbToLinear(intG), srgbToLinear(intB)};
    }

    Color
    decodeDC(std::string_view value) {
        if (value.size() != 4)
            throw std::invalid_argument("decode DC value size != 4");
        return decodeDC(decode83(value));
    }

    int
    encodeDC(const Color &c) {
        return (linearToSrgb(c.r) << 16) + (linearToSrgb(c.g) << 8) + linearToSrgb(c.b);
    }

    float
    signPow(float value, float exp) {
        return std::copysign(std::pow(std::abs(value), exp), value);
    }

    int
    encodeAC(const Color &c, float maximumValue) {
        auto quantR =
                int(std::clamp(std::floor(signPow(c.r / maximumValue, 0.5) * 9 + 9.5), 0., 18.));
        auto quantG =
                int(std::clamp(std::floor(signPow(c.g / maximumValue, 0.5) * 9 + 9.5), 0., 18.));
        auto quantB =
                int(std::clamp(std::floor(signPow(c.b / maximumValue, 0.5) * 9 + 9.5), 0., 18.));

        return quantR * 19 * 19 + quantG * 19 + quantB;
    }

    Color
    decodeAC(int value, float maximumValue) {
        auto quantR = value / (19 * 19);
        auto quantG = (value / 19) % 19;
        auto quantB = value % 19;

        return {signPow((float(quantR) - 9) / 9, 2) * maximumValue,
                signPow((float(quantG) - 9) / 9, 2) * maximumValue,
                signPow((float(quantB) - 9) / 9, 2) * maximumValue};
    }

    Color
    decodeAC(std::string_view value, float maximumValue) {
        return decodeAC(decode83(value), maximumValue);
    }

    std::vector<float>
    bases_for(uint dimension, uint components) {
        std::vector<float> bases(dimension * components, 0.f);
        auto scale = M_PI / float(dimension);
        for (uint x = 0; x < dimension; x++) {
            for (uint nx = 0; nx < components; nx++) {
                bases[x * components + nx] = std::cosf(static_cast<float>(scale) * float(nx * x));
            }
        }
        return bases;
    }
}

namespace blurhash {
    Image
    decode(std::string_view blurhash, uint width, uint height, uint bytesPerPixel) {
        if (blurhash.length() < 6)
            throw std::invalid_argument("blurhash string invalid, too short.");

        if (width < 1 || height < 1)
            throw std::invalid_argument("width and height must be greater than 1.");

        Image i{};

        std::vector<Color> values;
        values.reserve(blurhash.size() / 2);

        Components components = unpackComponents(decode83(blurhash.substr(0, 1)));

        if (components.x < 1 || components.y < 1 ||
            blurhash.size() != lround(1 + 1 + 4 + (components.x * components.y - 1) * 2))
            throw std::invalid_argument("decoded components invalid");

        auto maxAC = decodeMaxAC(blurhash.substr(1, 1));
        Color average = decodeDC(blurhash.substr(2, 4));

        values.push_back(average);
        for (size_t c = 6; c < blurhash.size(); c += 2)
            values.push_back(decodeAC(blurhash.substr(c, 2), maxAC));

        i.image = decltype(i.image)(height * width * bytesPerPixel, 255);

        std::vector<float> basis_x = bases_for(width, components.x);
        std::vector<float> basis_y = bases_for(height, components.y);

        for (uint y = 0; y < height; y++) {
            for (uint x = 0; x < width; x++) {
                Color c{};

                for (uint nx = 0; nx < components.x; nx++) {
                    for (uint ny = 0; ny < components.y; ny++) {
                        float basis = basis_x[x * components.x + nx] *
                                      basis_y[y * components.y + ny];
                        c += values[nx + ny * components.x] * basis;
                    }
                }

                i.image[(y * width + x) * bytesPerPixel + 0] = linearToSrgb(c.r);
                i.image[(y * width + x) * bytesPerPixel + 1] = linearToSrgb(c.g);
                i.image[(y * width + x) * bytesPerPixel + 2] = linearToSrgb(c.b);
            }
        }

        i.height = height;
        i.width = width;

        return i;
    }

    std::string
    encode(uint8_t *image,
           uint width,
           uint height,
           uint components_x,
           uint components_y,
           uint bytesPerPixel) {

        if (width < 1 || height < 1)
            throw std::invalid_argument("height and width must be greater than 1.");

        if (components_x > 9 || components_x < 1 || components_y > 9 || components_y < 1)
            throw std::invalid_argument("components must be in the range of 1-9.");

        if (!image)
            throw std::invalid_argument("must provide valid image argument.");

        std::vector<float> basis_x = bases_for(width, components_x);
        std::vector<float> basis_y = bases_for(height, components_y);

        std::vector<Color> factors(components_x * components_y, Color{});
        for (uint y = 0; y < height; y++) {
            for (uint x = 0; x < width; x++) {
                Color linear{srgbToLinear(image[3 * x + 0 + y * width * bytesPerPixel]),
                             srgbToLinear(image[3 * x + 1 + y * width * bytesPerPixel]),
                             srgbToLinear(image[3 * x + 2 + y * width * bytesPerPixel])};

                // other half of normalization.
                linear *= 1.f / static_cast<float>(width);

                for (uint ny = 0; ny < components_y; ny++) {
                    for (uint nx = 0; nx < components_x; nx++) {
                        float basis = basis_x[x * components_x + nx] *
                                      basis_y[y * components_y + ny];
                        factors[ny * components_x + nx] += linear * basis;
                    }
                }
            }
        }

        // scale by normalization. Half the scaling is done in the previous loop to prevent going
        // too far outside the float range.
        for (size_t i = 0; i < factors.size(); i++) {
            float normalisation = (i == 0) ? 1 : 2;
            float scale = normalisation / static_cast<float>(height);
            factors[i] *= scale;
        }

        if (factors.empty())
            throw std::length_error("error calculating factors.");

        auto dc = factors.front();
        factors.erase(factors.begin());

        std::string h;

        h += leftPad(encode83(packComponents({components_x, components_y})), 1);

        float maximumValue;
        if (!factors.empty()) {
            float actualMaximumValue = 0;
            for (auto ac: factors) {
                actualMaximumValue = std::max({
                                                      std::abs(ac.r),
                                                      std::abs(ac.g),
                                                      std::abs(ac.b),
                                                      actualMaximumValue,
                                              });
            }

            int quantisedMaximumValue = encodeMaxAC(actualMaximumValue);
            maximumValue = ((float) quantisedMaximumValue + 1) / 166;
            h += leftPad(encode83(quantisedMaximumValue), 1);
        } else {
            maximumValue = 1;
            h += leftPad(encode83(0), 1);
        }

        h += leftPad(encode83(encodeDC(dc)), 4);

        for (auto ac: factors)
            h += leftPad(encode83(encodeAC(ac, maximumValue)), 2);

        return h;
    }
}
