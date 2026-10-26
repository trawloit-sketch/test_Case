<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     * Tabel customers — menyimpan data pelanggan ERP
     */
    public function up(): void
    {
        Schema::create('customers', function (Blueprint $table) {
            $table->id();
            $table->string('customer_code', 20)->unique()->comment('Kode unik pelanggan, contoh: CUST-001');
            $table->string('company_name', 150)->comment('Nama perusahaan / toko pelanggan');
            $table->string('contact_name', 100)->nullable()->comment('Nama PIC / kontak utama');
            $table->string('email', 150)->nullable()->comment('Email kontak pelanggan');
            $table->string('phone', 20)->nullable()->comment('Nomor telepon pelanggan');
            $table->text('address')->nullable()->comment('Alamat lengkap pelanggan');
            $table->string('city', 100)->nullable()->comment('Kota');
            $table->string('province', 100)->nullable()->comment('Provinsi');
            $table->string('postal_code', 10)->nullable()->comment('Kode pos');
            $table->decimal('credit_limit', 15, 2)->default(0)->comment('Batas kredit dalam rupiah');
            $table->unsignedTinyInteger('payment_terms_days')->default(30)->comment('Jangka waktu pembayaran dalam hari');
            $table->boolean('is_active')->default(true)->comment('Status aktif pelanggan');
            $table->timestamps();
            $table->softDeletes();

            // Index untuk pencarian cepat
            $table->index('company_name');
            $table->index('city');
            $table->index('is_active');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('customers');
    }
};
