    static RomanNumber INumberBase<RomanNumber>.One => throw new NotImplementedException();
    static int INumberBase<RomanNumber>.Radix => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.Zero => throw new NotImplementedException();
    static RomanNumber IAdditiveIdentity<RomanNumber, RomanNumber>.AdditiveIdentity => throw new NotImplementedException();
    static RomanNumber IMultiplicativeIdentity<RomanNumber, RomanNumber>.MultiplicativeIdentity => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.Abs(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsCanonical(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsComplexNumber(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsEvenInteger(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsFinite(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsImaginaryNumber(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsInfinity(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsInteger(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsNaN(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsNegative(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsNegativeInfinity(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsNormal(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsOddInteger(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsPositive(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsPositiveInfinity(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsRealNumber(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsSubnormal(RomanNumber value) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.IsZero(RomanNumber value) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.MaxMagnitude(RomanNumber x, RomanNumber y) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.MaxMagnitudeNumber(RomanNumber x, RomanNumber y) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.MinMagnitude(RomanNumber x, RomanNumber y) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.MinMagnitudeNumber(RomanNumber x, RomanNumber y) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.Parse(ReadOnlySpan<char> s, NumberStyles style, IFormatProvider? provider) => throw new NotImplementedException();
    static RomanNumber INumberBase<RomanNumber>.Parse(string s, NumberStyles style, IFormatProvider? provider) => throw new NotImplementedException();
    static RomanNumber ISpanParsable<RomanNumber>.Parse(ReadOnlySpan<char> s, IFormatProvider? provider) => throw new NotImplementedException();
    static RomanNumber IParsable<RomanNumber>.Parse(string s, IFormatProvider? provider) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertFromChecked<TOther>(TOther value, out RomanNumber result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertFromSaturating<TOther>(TOther value, out RomanNumber result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertFromTruncating<TOther>(TOther value, out RomanNumber result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertToChecked<TOther>(RomanNumber value, out TOther result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertToSaturating<TOther>(RomanNumber value, out TOther result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryConvertToTruncating<TOther>(RomanNumber value, out TOther result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryParse(ReadOnlySpan<char> s, NumberStyles style, IFormatProvider? provider, out RomanNumber result) => throw new NotImplementedException();
    static bool INumberBase<RomanNumber>.TryParse(string? s, NumberStyles style, IFormatProvider? provider, out RomanNumber result) => throw new NotImplementedException();
    static bool ISpanParsable<RomanNumber>.TryParse(ReadOnlySpan<char> s, IFormatProvider? provider, out RomanNumber result) => throw new NotImplementedException();
    static bool IParsable<RomanNumber>.TryParse(string? s, IFormatProvider? provider, out RomanNumber result) => throw new NotImplementedException();
    int IComparable.CompareTo(object? obj) => throw new NotImplementedException();
    int IComparable<RomanNumber>.CompareTo(RomanNumber other) => throw new NotImplementedException();
    bool IEquatable<RomanNumber>.Equals(RomanNumber other) => throw new NotImplementedException();
    string IFormattable.ToString(string? format, IFormatProvider? formatProvider) => throw new NotImplementedException();
    bool ISpanFormattable.TryFormat(Span<char> destination, out int charsWritten, ReadOnlySpan<char> format, IFormatProvider? provider) => throw new NotImplementedException();
    static RomanNumber IUnaryPlusOperators<RomanNumber, RomanNumber>.operator +(RomanNumber value) => throw new NotImplementedException();
    static RomanNumber IAdditionOperators<RomanNumber, RomanNumber, RomanNumber>.operator +(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static RomanNumber IUnaryNegationOperators<RomanNumber, RomanNumber>.operator -(RomanNumber value) => throw new NotImplementedException();
    static RomanNumber ISubtractionOperators<RomanNumber, RomanNumber, RomanNumber>.operator -(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static RomanNumber IIncrementOperators<RomanNumber>.operator ++(RomanNumber value) => throw new NotImplementedException();
    static RomanNumber IDecrementOperators<RomanNumber>.operator --(RomanNumber value) => throw new NotImplementedException();
    static RomanNumber IMultiplyOperators<RomanNumber, RomanNumber, RomanNumber>.operator *(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static RomanNumber IDivisionOperators<RomanNumber, RomanNumber, RomanNumber>.operator /(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static RomanNumber IModulusOperators<RomanNumber, RomanNumber, RomanNumber>.operator %(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IEqualityOperators<RomanNumber, RomanNumber, bool>.operator ==(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IEqualityOperators<RomanNumber, RomanNumber, bool>.operator !=(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IComparisonOperators<RomanNumber, RomanNumber, bool>.operator <(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IComparisonOperators<RomanNumber, RomanNumber, bool>.operator >(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IComparisonOperators<RomanNumber, RomanNumber, bool>.operator <=(RomanNumber left, RomanNumber right) => throw new NotImplementedException();
    static bool IComparisonOperators<RomanNumber, RomanNumber, bool>.operator >=(RomanNumber left, RomanNumber right) => throw new NotImplementedException();